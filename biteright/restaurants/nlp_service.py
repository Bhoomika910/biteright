# Semantic allergy detection using sentence-transformers.
# Falls back gracefully if the library is not installed.

_model = None

def _get_model():
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            _model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception:
            _model = 'unavailable'
    return _model


def detect_allergy_risk(user_allergies, ingredients):
    allergy_texts    = [str(a).lower() for a in user_allergies]
    ingredient_texts = [str(i).lower() for i in ingredients]

    if not allergy_texts or not ingredient_texts:
        return False

    model = _get_model()
    if model == 'unavailable':
        # Fallback: simple substring match
        for allergy in allergy_texts:
            for ingredient in ingredient_texts:
                if allergy in ingredient:
                    return True
        return False

    from sentence_transformers import util
    allergy_emb    = model.encode(allergy_texts,    convert_to_tensor=True)
    ingredient_emb = model.encode(ingredient_texts, convert_to_tensor=True)
    scores         = util.cos_sim(allergy_emb, ingredient_emb)
    return float(scores.max()) > 0.6
