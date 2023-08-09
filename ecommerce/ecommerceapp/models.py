from django.db import models

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    desc = models.TextField(max_length=100)
    phone = models.IntegerField()

    def __str__(self):
        return self.name
    
# Products
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=150)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=150)
    image = models.ImageField(upload_to="images/product")

    def __str__(self):
        return self.product_name
    



