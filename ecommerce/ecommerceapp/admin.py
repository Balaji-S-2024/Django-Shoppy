from django.contrib import admin
from ecommerceapp import models

# Register your models here.
admin.site.register(models.Contact)
admin.site.register(models.Product)
admin.site.register(models.Order)
admin.site.register(models.OrderUpdate)