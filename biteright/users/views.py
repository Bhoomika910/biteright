from rest_framework.views    import APIView
from rest_framework.response import Response
from rest_framework          import status
from .models                 import UserProfile, UserAddress
from .serializers            import UserProfileSerializer, UserAddressSerializer


class UserListCreateView(APIView):

    def get(self, request):
        users      = UserProfile.objects.all().order_by('-created_at')
        serializer = UserProfileSerializer(users, many=True)
        return Response({'status': 'success', 'data': serializer.data})

    def post(self, request):
        # Idempotent: return existing user if email already registered
        email = request.data.get('email', '').strip().lower()
        if email:
            existing = UserProfile.objects.filter(email=email).first()
            if existing:
                return Response(
                    {
                        'status':  'success',
                        'message': 'Welcome back!',
                        'data':    UserProfileSerializer(existing).data,
                    },
                    status=status.HTTP_200_OK,
                )

        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'status':  'success',
                    'message': 'Profile created!',
                    'data':    serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {'status': 'error', 'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserDetailView(APIView):

    def get(self, request, pk):
        try:
            user = UserProfile.objects.get(pk=pk)
        except UserProfile.DoesNotExist:
            return Response(
                {'status': 'error', 'message': 'User not found'},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response({'status': 'success', 'data': UserProfileSerializer(user).data})


class AddressView(APIView):
    """
    GET /api/users/<user_id>/addresses/
    POST /api/users/<user_id>/addresses/
    """
    def get(self, request, user_id):
        adds = UserAddress.objects.filter(user_id=user_id)
        serializer = UserAddressSerializer(adds, many=True)
        return Response({'status': 'success', 'data': serializer.data})

    def post(self, request, user_id):
        data = request.data.copy()
        data['user'] = user_id
        serializer = UserAddressSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'status': 'error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# FIX Bug 3: urls.py imports CreateUserProfileView — alias resolves the ImportError
CreateUserProfileView = UserListCreateView
