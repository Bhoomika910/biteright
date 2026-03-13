from rest_framework.views    import APIView
from rest_framework.response import Response
from rest_framework          import status
from .models                 import Order
from .serializers            import OrderSerializer, OrderCreateSerializer


class OrderListCreateView(APIView):

    def get(self, request):
        """GET /api/orders/?user=<id>"""
        user_id = request.query_params.get('user')
        if not user_id:
            return Response(
                {'status': 'error', 'message': 'Provide ?user=<id>'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        orders     = Order.objects.filter(user_id=user_id).prefetch_related('order_items__menu_item')
        serializer = OrderSerializer(orders, many=True)
        return Response({'status': 'success', 'data': serializer.data})

    def post(self, request):
        """POST /api/orders/"""
        serializer = OrderCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'status': 'error', 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        order = serializer.save()
        return Response(
            {
                'status':  'success',
                'message': 'Order placed successfully!',
                'data':    OrderSerializer(order).data,
            },
            status=status.HTTP_201_CREATED,
        )
