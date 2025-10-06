from django.contrib import admin
from.models import Customer
from.models import Restaurant
from.models import MenuItem

# Register your models here.
from .models import Customer, Restaurant, MenuItem
admin.site.register(Customer)
admin.site.register(Restaurant)
admin.site.register(MenuItem)
