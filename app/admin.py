from django.contrib import admin
from .models import Contact,ProductItems,MyOrders
# Register your models here.
admin.site.register(Contact)
admin.site.register(ProductItems)
admin.site.register(MyOrders)