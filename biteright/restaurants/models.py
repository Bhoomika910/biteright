from django.db import models

class Category(models.Model):
    name        = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    name                   = models.CharField(max_length=120)
    description            = models.TextField(blank=True, help_text="Short bio of the restaurant")
    cuisine_type           = models.CharField(max_length=100, blank=True, default="Multicuisine")
    location               = models.CharField(max_length=255, blank=True)
    contact_number         = models.CharField(max_length=15, blank=True)
    official_email         = models.EmailField(blank=True)
    image_url              = models.URLField(blank=True)
    rating                 = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    delivery_time          = models.CharField(max_length=20, default="30-40 min")
    opening_time           = models.TimeField(null=True, blank=True)
    closing_time           = models.TimeField(null=True, blank=True)
    is_active              = models.BooleanField(default=True)
    supports_customization = models.BooleanField(default=True)
    created_at             = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    restaurant   = models.ForeignKey(
        'Restaurant', on_delete=models.CASCADE, related_name='menu_items',
    )
    name         = models.CharField(max_length=100, db_index=True)
    price        = models.DecimalField(max_digits=10, decimal_places=2)
    description  = models.TextField(blank=True)
    is_veg       = models.BooleanField(default=True)
    diet_tags    = models.CharField(max_length=200, blank=True, help_text="Extra tags like Vegan, Gluten-Free")
    category     = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='items')
    ingredients  = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.restaurant.name})"


class Review(models.Model):
    user        = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, related_name='reviews')
    restaurant  = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='reviews')
    menu_item   = models.ForeignKey('MenuItem', on_delete=models.SET_NULL, null=True, blank=True)
    rating      = models.PositiveSmallIntegerField(default=5)  # 1-5 stars
    comment     = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name}'s review of {self.restaurant.name}"
