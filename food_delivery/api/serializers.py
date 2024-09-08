from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import Restaurant, Category, MenuItem, Order

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'restaurant']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'restaurant', 'items', 'total_price', 'payment_method', 'created_at']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')  # Get items
        total_price = sum(item.price for item in items_data)  # Calculate total price
        order = Order.objects.create(total_price=total_price, **validated_data)  # Create order
        order.items.set(items_data)  # Set items for the order
        return order


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'  # Or specify the fields you want


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'  # or specify the fields you need
