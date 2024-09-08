from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User model extending AbstractUser to include roles (owner, employee) and association with Restaurant
class User(AbstractUser):
    ROLE_CHOICES = (
        ('owner', 'Owner'),
        ('employee', 'Employee'),
    )
    
    # Role can be either 'owner' or 'employee'
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    
    
    restaurant = models.ForeignKey('Restaurant', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username

# Restaurant model with name and location fields
class Restaurant(models.Model):
    name = models.CharField(max_length=255)  
    location = models.CharField(max_length=255)  

    def __str__(self):
        return self.name  # Display restaurant name in the admin interface

# Category model which is associated with a Restaurant
class Category(models.Model):
    name = models.CharField(max_length=255)  # Name of the category (e.g., Appetizers, Desserts)
    
    # ForeignKey to Restaurant, with cascading delete (deleting restaurant will delete related categories)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.name  

# MenuItem model representing individual items in a menu, associated with a Category
class MenuItem(models.Model):
    name = models.CharField(max_length=255)  # Name of the menu item (e.g., Burger, Pizza)
    
    # ForeignKey to Category, with cascading delete (deleting category will delete related menu items)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)  

    def __str__(self):
        return self.name  # Display item name in the admin interface

# Order model representing customer orders
class Order(models.Model):
    PAYMENT_CHOICES = (
        ('card', 'Card'),
        ('cash', 'Cash'),
    )
    
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # ForeignKey to Restaurant, linking the order to a restaurant
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    
    
    items = models.ManyToManyField(MenuItem)
    
    # Total price of the order
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Payment method for the order (card or cash)
    payment_method = models.CharField(max_length=4, choices=PAYMENT_CHOICES)
    
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id} by {self.user}'  # Display order details in the admin interface
