from django.contrib import admin
from .models import User, Restaurant, Category, MenuItem, Order

admin.site.register(User)
admin.site.register(Restaurant)
admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Order)
