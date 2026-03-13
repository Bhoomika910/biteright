from django.db import models

MOOD_CHOICES = [
    ('comfort',    'Comfort'),
    ('healthy',    'Healthy'),
    ('cheat',      'Cheat Meal'),
    ('spicy',      'Spicy'),
    ('late-night', 'Late Night'),
]

class Restaurant(models.Model):
    name                   = models.CharField(max_length=120)
    image_url              = models.URLField(blank=True)
    supports_customization = models.BooleanField(default=True)
    created_at             = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    restaurant  = models.ForeignKey(
        'Restaurant', on_delete=models.CASCADE, related_name='menu_items',
    )
    name        = models.CharField(max_length=100)
    price       = models.FloatField()
    diet_tags   = models.CharField(max_length=200, blank=True)
    mood_tags   = models.CharField(max_length=50, choices=MOOD_CHOICES, blank=True)
    ingredients = models.TextField(blank=True)

    def __str__(self):
        return self.name
