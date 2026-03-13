from django.db import models

class UserProfile(models.Model):
    name             = models.CharField(max_length=100)
    email            = models.EmailField(unique=True)
    allergies        = models.TextField(blank=True)
    diet_preferences = models.TextField(blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
