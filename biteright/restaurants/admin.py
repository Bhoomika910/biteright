from django.contrib import admin
from .models import MenuItem, Restaurant, Review

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cuisine_type', 'rating', 'delivery_time', 'location')
    search_fields = ('name', 'cuisine_type')

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'restaurant', 'diet_tags', 'mood_tags')
    list_filter = ('diet_tags', 'mood_tags', 'restaurant')
    search_fields = ('name', 'ingredients')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'restaurant', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
