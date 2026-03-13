# orders/models.py
# FIX Bug 1: Renamed total_amount → total_price, order_time → created_at.
# FIX Bug 2: Added OrderItem model (table was missing entirely from DB).
# After replacing this file run:
#   python manage.py migrate orders zero
#   python manage.py makemigrations orders
#   python manage.py migrate

from django.db import models
from users.models import UserProfile
from restaurants.models import MenuItem, Restaurant


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending',          'Pending'),
        ('preparing',        'Preparing'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered',        'Delivered'),
        ('cancelled',        'Cancelled'),
    ]

    user        = models.ForeignKey(UserProfile,  on_delete=models.CASCADE,  related_name='orders')
    restaurant  = models.ForeignKey(Restaurant,   on_delete=models.SET_NULL, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.id} — {self.user.name} — {self.status}'

    def recalculate_total(self):
        total           = sum(item.subtotal() for item in self.order_items.all())
        self.total_price = total
        self.save(update_fields=['total_price'])


class OrderItem(models.Model):
    order     = models.ForeignKey(Order,    on_delete=models.CASCADE,  related_name='order_items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True)
    quantity  = models.PositiveIntegerField(default=1)
    price     = models.DecimalField(max_digits=8, decimal_places=2)  # snapshot at order time

    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        name = self.menu_item.name if self.menu_item else 'deleted item'
        return f'{self.quantity}x {name}'
