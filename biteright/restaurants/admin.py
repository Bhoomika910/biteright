from django.contrib import admin
from .models import MenuItem, Restaurant, Review, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cuisine_type', 'rating', 'delivery_time', 'location', 'is_active')
    list_filter = ('is_active', 'cuisine_type')
    search_fields = ('name', 'cuisine_type', 'location')

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'restaurant', 'category', 'is_veg', 'is_available')
    list_filter = ('is_veg', 'is_available', 'category', 'restaurant')
    search_fields = ('name', 'ingredients')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'restaurant', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
