from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from .models import User
from rest_framework import viewsets
from .models import Restaurant, Category, MenuItem, Order
from .serializers import CategorySerializer, MenuItemSerializer, OrderSerializer
from .permissions import IsOwnerOrEmployee

# User Registration View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()  # Queryset for all users
    serializer_class = RegisterSerializer  # Serializer to handle user registration

    # Overriding the create method to add token generation upon registration
    def create(self, request, *args, **kwargs):
        # Calling the parent class's create method to handle user creation
        response = super().create(request, *args, **kwargs)
        
        # After the user is created, `self.object` will hold the user instance
        token = Token.objects.create(user=self.object)  # Generate auth token for the user

        # Adding the token to the response data
        user = response.data  # Getting the response data (user info)
        user['token'] = token.key  # Add the token to the response data

        return Response(user)  # Return the user data along with the token


# User Login View
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer  

    # Handling POST request for login
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)  # Validate login data
        serializer.is_valid(raise_exception=True)  

        user = serializer.validated_data  # Get the authenticated user from validated data
        token, created = Token.objects.get_or_create(user=user)  # Get or create a token for the user
        
        # Return the token and user details in the response
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data  
        })


# Category ViewSet for managing restaurant categories
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()  
    serializer_class = CategorySerializer  
    permission_classes = [IsOwnerOrEmployee]  


# MenuItem ViewSet for managing menu items
class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()  
    serializer_class = MenuItemSerializer  
    permission_classes = [IsOwnerOrEmployee]  


# Order ViewSet for handling customer orders
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()  
    serializer_class = OrderSerializer  
    permission_classes = [permissions.IsAuthenticated]  

    # Overriding the create method to automatically assign the user and restaurant to the order
    def perform_create(self, serializer):
        # Automatically set the user and the restaurant (from the user's restaurant field)
        serializer.save(user=self.request.user, restaurant=self.request.user.restaurant)
