# restaurants/views.py
# FIX Bug 4: All views imported by urls.py are now defined here.
# Includes: RestaurantListView, MenuItemListView, AllergyCheckView,
#           SearchMenuView, SafeMenuView, RecommendationView (lazy ML + fallback)

from rest_framework.views    import APIView
from rest_framework.response import Response
from rest_framework          import status

from .models       import Restaurant, MenuItem
from .serializers  import RestaurantSerializer, MenuItemSerializer
from .utils        import check_allergy_risk
from users.models  import UserProfile


# ── Restaurants ────────────────────────────────────────────────────────────────

class RestaurantListView(APIView):
    """GET /api/restaurants/"""
    def get(self, request):
        restaurants = Restaurant.objects.all().order_by('id')
        serializer  = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)


# ── Menu ───────────────────────────────────────────────────────────────────────

class MenuItemListView(APIView):
    """GET /api/restaurants/<restaurant_id>/menu/"""
    def get(self, request, restaurant_id):
        items      = MenuItem.objects.filter(restaurant_id=restaurant_id)
        serializer = MenuItemSerializer(items, many=True)
        return Response(serializer.data)


# ── Allergy check ──────────────────────────────────────────────────────────────

class AllergyCheckView(APIView):
    """
    POST /api/check-allergy/
    Body: { "allergies": ["peanuts"], "ingredients": ["flour", "peanut oil"] }
    """
    def post(self, request):
        allergies   = request.data.get('allergies', [])
        ingredients = request.data.get('ingredients', [])
        risk        = check_allergy_risk(allergies, ingredients)
        return Response({'allergy_risk': risk})


# ── Menu search ────────────────────────────────────────────────────────────────

class SearchMenuView(APIView):
    """GET /api/search-menu/?q=<query>"""
    def get(self, request):
        q = request.query_params.get('q', '').strip()
        if not q:
            return Response([])
        items = (
            MenuItem.objects.filter(name__icontains=q) |
            MenuItem.objects.filter(ingredients__icontains=q)
        ).distinct()
        serializer = MenuItemSerializer(items, many=True)
        return Response(serializer.data)


# ── Safe menu (allergen-filtered for a specific user) ─────────────────────────

class SafeMenuView(APIView):
    """GET /api/safe-menu/<user_id>/<restaurant_id>/"""
    def get(self, request, user_id, restaurant_id):
        try:
            user = UserProfile.objects.get(pk=user_id)
        except UserProfile.DoesNotExist:
            return Response(
                {'status': 'error', 'message': f'User {user_id} not found'},
                status=status.HTTP_404_NOT_FOUND,
            )
        items     = MenuItem.objects.filter(restaurant_id=restaurant_id)
        allergens = [a.strip().lower() for a in (user.allergies or '').split(',') if a.strip()]
        if allergens:
            safe = [i for i in items
                    if not check_allergy_risk(allergens, i.ingredients.split(','))]
        else:
            safe = list(items)
        serializer = MenuItemSerializer(safe, many=True)
        return Response({'status': 'success', 'data': serializer.data})


# ── Recommendations (lazy ML + keyword fallback) ───────────────────────────────

_encoder = None  # loaded on first request

def _get_encoder():
    global _encoder
    if _encoder is None:
        try:
            from sentence_transformers import SentenceTransformer
            _encoder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            print('[BiteRight] ✅ ML model loaded.')
        except Exception as e:
            print(f'[BiteRight] ⚠️  ML model unavailable ({e}). Using keyword fallback.')
            _encoder = 'fallback'
    return _encoder


def _cosine_sim(a, b):
    import numpy as np
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    return float(np.dot(a, b) / denom) if denom else 0.0


def _score_ml(dish_text, query_emb, encoder):
    dish_emb = encoder.encode(dish_text, convert_to_numpy=True)
    return _cosine_sim(query_emb, dish_emb)


def _score_fallback(dish, mood, diet, time_of_day):
    score = 0
    text  = f"{dish.name} {dish.mood_tags or ''} {dish.diet_tags or ''} {dish.ingredients or ''}".lower()

    if mood and mood.lower().replace('_', ' ') in text:
        score += 10
    if diet:
        d = diet.lower()
        if 'veg' in d and 'veg' in text:
            score += 8
        elif 'non' in d and any(k in text for k in ['chicken', 'meat', 'egg']):
            score += 8

    time_keywords = {
        'morning':    ['light', 'idli', 'dosa', 'poha', 'upma', 'toast', 'egg'],
        'afternoon':  ['rice', 'dal', 'curry', 'thali', 'roti'],
        'night':      ['curry', 'biryani', 'naan', 'paneer', 'butter'],
        'late_night': ['soup', 'sandwich', 'snack', 'maggi', 'noodle'],
    }
    for kw in time_keywords.get(time_of_day or '', []):
        if kw in text:
            score += 4
            break
    if 'comfort' in text:
        score += 2
    return score


class RecommendationView(APIView):
    """
    GET /api/recommendations/<user_id>/<restaurant_id>/?mood=comfort&time=afternoon
    Returns up to 10 dishes ranked by ML similarity + keyword heuristics,
    filtered for the user's allergens.
    """
    def get(self, request, user_id, restaurant_id):
        mood        = request.query_params.get('mood', '')
        time_of_day = request.query_params.get('time', '')

        try:
            user = UserProfile.objects.get(pk=user_id)
        except UserProfile.DoesNotExist:
            return Response(
                {'status': 'error', 'message': f'User {user_id} not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        dishes = MenuItem.objects.filter(restaurant_id=restaurant_id)
        if not dishes.exists():
            return Response({'status': 'success', 'recommended_items': []})

        diet_label = user.diet_preferences or ''
        query      = f"{mood.replace('_', ' ')} food {diet_label} {time_of_day} meal"
        encoder    = _get_encoder()
        scored     = []

        if encoder != 'fallback':
            try:
                query_emb = encoder.encode(query, convert_to_numpy=True)
                for dish in dishes:
                    dish_text = f"{dish.name} {dish.mood_tags or ''} {dish.diet_tags or ''} {dish.ingredients or ''}"
                    sim   = _score_ml(dish_text, query_emb, encoder)
                    bonus = _score_fallback(dish, mood, diet_label, time_of_day)
                    scored.append((dish, round(sim * 20 + bonus, 2)))
            except Exception as e:
                print(f'[BiteRight] ML scoring error: {e}. Falling back.')
                encoder = 'fallback'

        if encoder == 'fallback':
            for dish in dishes:
                scored.append((dish, _score_fallback(dish, mood, diet_label, time_of_day)))

        # Filter allergens
        allergens = [a.strip().lower() for a in (user.allergies or '').split(',') if a.strip()]
        if allergens:
            scored = [
                (d, s) for d, s in scored
                if not any(a in (d.ingredients or '').lower() for a in allergens)
            ]

        scored.sort(key=lambda x: x[1], reverse=True)

        result = [
            {
                'id':          dish.id,
                'name':        dish.name,
                'price':       float(dish.price),
                'diet_tags':   dish.diet_tags,
                'mood_tags':   dish.mood_tags,
                'ingredients': dish.ingredients,
                'score':       score,
            }
            for dish, score in scored[:10]
        ]
        return Response({'status': 'success', 'recommended_items': result})
