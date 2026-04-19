from rest_framework import serializers
from .models import UserProfile, UserAddress

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model  = UserProfile
        fields = '__all__'

class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model  = UserAddress
        fields = '__all__'
