from rest_framework import generics
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import User
from django.contrib.auth import authenticate

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"detail": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            # Get the user by email
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid Credentials'}, status=400)

        # Authenticate using the username from the user found by email
        user = authenticate(request, username=user.username, password=password)
        
        if user is not None:
            # For session-based authentication, we log the user in
            return Response({'message': 'Login successful!'}, status=200)
        
        return Response({'error': 'Invalid Credentials'}, status=400)
