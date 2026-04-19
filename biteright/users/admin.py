from django.contrib import admin
from .models import UserProfile, UserAddress

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'allergies', 'diet_preferences', 'created_at')

@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'address_type', 'address_line', 'city', 'state', 'pincode', 'phone_number')
    list_filter = ('address_type', 'city', 'state')
