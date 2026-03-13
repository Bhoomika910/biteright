from rest_framework import serializers
from .models import Order, OrderItem
from restaurants.models import MenuItem


class OrderItemReadSerializer(serializers.ModelSerializer):
    dish_name = serializers.SerializerMethodField()
    price     = serializers.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        model  = OrderItem
        fields = ['id', 'menu_item', 'dish_name', 'quantity', 'price']

    def get_dish_name(self, obj):
        return obj.menu_item.name if obj.menu_item else 'Deleted item'


class OrderItemWriteSerializer(serializers.Serializer):
    menu_item = serializers.IntegerField()
    quantity  = serializers.IntegerField(min_value=1, default=1)


class OrderSerializer(serializers.ModelSerializer):
    items      = OrderItemReadSerializer(source='order_items', many=True, read_only=True)
    status     = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model  = Order
        fields = ['id', 'user', 'restaurant', 'total_price', 'status', 'items', 'created_at']


class OrderCreateSerializer(serializers.Serializer):
    """Accepts the exact payload the frontend sends."""
    user        = serializers.IntegerField()
    restaurant  = serializers.IntegerField(required=False, allow_null=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, default=0)
    items       = OrderItemWriteSerializer(many=True)

    def validate_user(self, value):
        from users.models import UserProfile
        try:
            return UserProfile.objects.get(pk=value)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError(f'User {value} not found.')

    def validate_restaurant(self, value):
        if value is None:
            return None
        from restaurants.models import Restaurant
        try:
            return Restaurant.objects.get(pk=value)
        except Restaurant.DoesNotExist:
            return None

    def create(self, validated_data):
        user       = validated_data['user']
        restaurant = validated_data.get('restaurant')
        items_data = validated_data['items']
        total      = validated_data.get('total_price', 0)

        order = Order.objects.create(
            user=user, restaurant=restaurant, total_price=total,
        )

        for item_data in items_data:
            try:
                menu_item = MenuItem.objects.get(pk=item_data['menu_item'])
                OrderItem.objects.create(
                    order=order,
                    menu_item=menu_item,
                    quantity=item_data['quantity'],
                    price=menu_item.price,
                )
            except MenuItem.DoesNotExist:
                pass  # skip deleted items silently

        if not total:
            order.recalculate_total()

        return order
