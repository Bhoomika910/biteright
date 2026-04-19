import os
import django
import random

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from restaurants.models import Restaurant, MenuItem, Review, Category
from users.models import UserProfile, UserAddress

def seed_data():
    print("Cleaning old data...")
    UserAddress.objects.all().delete()
    Review.objects.all().delete()
    MenuItem.objects.all().delete()
    Restaurant.objects.all().delete()
    Category.objects.all().delete()

    # Create Categories
    cat_map = {}
    cat_list = ['Healthy', 'Comfort', 'Spicy', 'Cheat Meal', 'Late Night', 'Desserts', 'Breakfast']
    for cat_name in cat_list:
        cat_map[cat_name.lower()] = Category.objects.create(name=cat_name)
    
    user = UserProfile.objects.first()
    if not user:
        user = UserProfile.objects.create(
            name="Bhoomika M Bidari",
            email="bhoomika.m.bidari966@gmail.com",
            phone_number="9876543210",
            diet_preferences="vegetarian",
            allergies="Peanuts"
        )
    
    # Create an address
    UserAddress.objects.create(
        user=user,
        address_line="No 42, 2nd Main, Indiranagar",
        city="Bangalore",
        state="Karnataka",
        pincode="560038",
        phone_number="9876543210",
        is_default=True,
        address_type="Home"
    )

    restaurants_data = [
        {
            "name": "The Green Bowl", 
            "image_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd",
            "description": "Healthy, organic, and locally sourced salads and bowls.",
            "cuisine_type": "Healthy / Vegan",
            "location": "Indiranagar, Bangalore",
            "contact_number": "080-12345678",
            "official_email": "hello@greenbowl.com",
            "rating": 4.5,
            "delivery_time": "20-30 min"
        },
        {
            "name": "Spice Route", 
            "image_url": "https://images.unsplash.com/photo-1585937421612-70a008356fbe",
            "description": "Authentic Indian flavors from across the country.",
            "cuisine_type": "North Indian",
            "location": "Koramangala, Bangalore",
            "contact_number": "080-87654321",
            "official_email": "info@spiceroute.in",
            "rating": 4.2,
            "delivery_time": "35-45 min"
        },
        {
            "name": "Burger Haven", 
            "image_url": "https://images.unsplash.com/photo-1571091718767-18b5b1457add",
            "description": "The best messy burgers in town.",
            "cuisine_type": "American",
            "location": "HSR Layout, Bangalore",
            "contact_number": "080-11223344",
            "official_email": "burgers@haven.com",
            "rating": 4.0,
            "delivery_time": "15-25 min"
        },
        {
            "name": "Sushi Zen", 
            "image_url": "https://images.unsplash.com/photo-1579871494447-9811cf80d66c",
            "description": "Fresh, premium sushi and Japanese delights.",
            "cuisine_type": "Japanese",
            "location": "Lavelle Road, Bangalore",
            "contact_number": "080-55667788",
            "official_email": "zen@sushi.jp",
            "rating": 4.8,
            "delivery_time": "40-50 min"
        },
        {
            "name": "Pasta Paradiso", 
            "image_url": "https://images.unsplash.com/photo-1551183053-bf91a1d81141",
            "description": "Handmade pasta and wood-fired pizzas.",
            "cuisine_type": "Italian",
            "location": "Whitefield, Bangalore",
            "contact_number": "080-99887766",
            "official_email": "pasta@paradiso.it",
            "rating": 4.3,
            "delivery_time": "30-40 min"
        }
    ]

    items_data = {
        "The Green Bowl": [
            {"name": "Quinoa Salad", "price": 280, "description": "High protein quinoa with kale", "is_veg": True, "diet_tags": "Vegan", "category": cat_map['healthy'], "ingredients": "Quinoa, Kale, Chickpeas, Lemon, Olive Oil"},
            {"name": "Avocado Toast", "price": 320, "description": "Sourdough mashed with fresh avocados", "is_veg": True, "diet_tags": "Veg", "category": cat_map['healthy'], "ingredients": "Sourdough, Avocado, Chili Flakes, Seeds"},
            {"name": "Berry Smoothie Bowl", "price": 350, "description": "Mixed berries with almond milk", "is_veg": True, "diet_tags": "Vegan", "category": cat_map['healthy'], "ingredients": "Blueberries, Bananas, Almond Milk, Granola"}
        ],
        "Spice Route": [
            {"name": "Butter Chicken", "price": 450, "description": "Classic creamy gravy chicken", "is_veg": False, "diet_tags": "Non-Veg", "category": cat_map['comfort'], "ingredients": "Chicken, Butter, Cream, Tomato, Spices"},
            {"name": "Paneer Tikka Masala", "price": 380, "description": "Char-grilled paneer in spicy gravy", "is_veg": True, "diet_tags": "Veg", "category": cat_map['spicy'], "ingredients": "Paneer, Onion, Capsicum, Yogurt, Spices"},
            {"name": "Garlic Naan", "price": 80, "description": "Freshly baked clay oven bread", "is_veg": True, "diet_tags": "Veg", "category": cat_map['comfort'], "ingredients": "Flour, Yeast, Garlic, Butter"}
        ],
        "Burger Haven": [
            {"name": "Classic Cheeseburger", "price": 250, "description": "Juicy patty with melt cheese", "is_veg": False, "diet_tags": "Non-Veg", "category": cat_map['cheat meal'], "ingredients": "Beef Patty, Cheese, Lettuce, Tomato, Bun"},
            {"name": "Spicy Zinger Burger", "price": 280, "description": "Crispy fried chicken with sauce", "is_veg": False, "diet_tags": "Non-Veg", "category": cat_map['spicy'], "ingredients": "Crispy Chicken, Spicy Sauce, Lettuce, Bun"},
            {"name": "Loaded Fries", "price": 180, "description": "Fries topped with cheese sauce", "is_veg": True, "diet_tags": "Veg", "category": cat_map['cheat meal'], "ingredients": "Potato, Cheese Sauce, Jalapenos"}
        ],
        "Sushi Zen": [
            {"name": "Salmon Nigiri", "price": 550, "description": "Fresh salmon over vinegar rice", "is_veg": False, "diet_tags": "Non-Veg", "category": cat_map['healthy'], "ingredients": "Salmon, Rice, Wasabi"},
            {"name": "California Roll", "price": 480, "description": "Crab stick and avocado roll", "is_veg": False, "diet_tags": "Non-Veg", "category": cat_map['healthy'], "ingredients": "Crab Stick, Avocado, Cucumber, Seaweed"},
            {"name": "Miso Soup", "price": 150, "description": "Traditional soybean broth", "is_veg": True, "diet_tags": "Veg", "category": cat_map['healthy'], "ingredients": "Tofu, Seaweed, Green Onion, Miso Paste"}
        ],
        "Pasta Paradiso": [
            {"name": "Spaghetti Carbonara", "price": 420, "description": "Egg and cheese based pasta", "is_veg": False, "diet_tags": "Non-Veg", "category": cat_map['comfort'], "ingredients": "Spaghetti, Egg, Bacon, Parmesan, Black Pepper"},
            {"name": "Lasagna Bolognese", "price": 480, "description": "Layered pasta with meat sauce", "is_veg": False, "diet_tags": "Non-Veg", "category": cat_map['comfort'], "ingredients": "Beef, Pasta sheets, Tomato Sauce, Bechamel, Cheese"},
            {"name": "Pesto Penne", "price": 380, "description": "Basil pesto tossed penne", "is_veg": True, "diet_tags": "Veg", "category": cat_map['healthy'], "ingredients": "Penne, Basil Pesto, Parmesan, Pine Nuts"}
        ]
    }

    comments = [
        "Absolutely delicious, will order again!",
        "The flavor profile was amazing.",
        "A bit spicy for my taste, but very fresh.",
        "Authentic taste, reminded me of home.",
        "Healthy yet filling.",
        "Perfect comfort food for a rainy day.",
        "Best dessert I have had in a long time!"
    ]

    for rest_info in restaurants_data:
        rest = Restaurant.objects.create(**rest_info)
        items = items_data.get(rest.name, [])
        for item_info in items:
            mi = MenuItem.objects.create(restaurant=rest, **item_info)
            # Add some reviews
            Review.objects.create(
                user=user,
                restaurant=rest,
                menu_item=mi,
                rating=random.randint(4, 5),
                comment=random.choice(comments)
            )
            
    print(f"Successfully seeded {Restaurant.objects.count()} restaurants and {MenuItem.objects.count()} menu items.")

if __name__ == "__main__":
    seed_data()
