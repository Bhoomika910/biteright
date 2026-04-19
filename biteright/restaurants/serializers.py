from rest_framework import serializers
from .models import MenuItem, Restaurant, Review, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Category
        fields = '__all__'


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Restaurant
        fields = '__all__'


class MenuItemSerializer(serializers.ModelSerializer):
    restaurant    = serializers.PrimaryKeyRelatedField(read_only=True)
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model  = MenuItem
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.name')

    class Meta:
        model  = Review
        fields = '__all__'
