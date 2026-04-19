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
    PAYMENT_CHOICES = [
        ('pending', 'Pending'),
        ('paid',    'Paid'),
        ('failed',  'Failed'),
    ]

    user                 = models.ForeignKey(UserProfile,  on_delete=models.CASCADE,  related_name='orders')
    restaurant           = models.ForeignKey(Restaurant,   on_delete=models.SET_NULL, null=True, blank=True)
    delivery_address     = models.ForeignKey('users.UserAddress', on_delete=models.SET_NULL, null=True, blank=True)
    items_price          = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Sum of order items")
    delivery_charge      = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount             = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price          = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Final price after discount and charges")
    status               = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method       = models.CharField(max_length=50, default='UPI')
    payment_status       = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='pending')
    transaction_id       = models.CharField(max_length=100, blank=True, null=True)
    special_instructions = models.TextField(blank=True)
    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.id} — {self.user.name} — {self.status}'

    def recalculate_total(self):
        items_sum = sum(item.subtotal() for item in self.order_items.all())
        self.items_price = items_sum
        self.total_price = (items_sum + self.delivery_charge) - self.discount
        self.save(update_fields=['items_price', 'total_price'])


class OrderItem(models.Model):
    order     = models.ForeignKey(Order,    on_delete=models.CASCADE,  related_name='order_items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True)
    quantity  = models.PositiveIntegerField(default=1)
    price     = models.DecimalField(max_digits=8, decimal_places=2, help_text="Snapshot of price at time of order")

    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        name = self.menu_item.name if self.menu_item else 'deleted item'
        return f'{self.quantity}x {name}'
