from django.db import models

class UserProfile(models.Model):
    name             = models.CharField(max_length=100)
    email            = models.EmailField(unique=True)
    allergies        = models.TextField(blank=True)
    diet_preferences = models.TextField(blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class UserAddress(models.Model):
    user         = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='addresses')
    address_line = models.CharField(max_length=255)
    city         = models.CharField(max_length=100, default="Bangalore")
    pincode      = models.CharField(max_length=10)
    is_default   = models.BooleanField(default=False)
    address_type = models.CharField(max_length=20, default="Home") # Home, Office, Other

    def __str__(self):
        return f"{self.address_line}, {self.city}"
