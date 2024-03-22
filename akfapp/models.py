from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Product(models.Model):
    Product_id = models.AutoField
    Product_name = models.CharField(max_length=300)
    category = models.CharField(max_length=300,default="")
    subcategory = models.CharField(max_length=200,default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    image = models.URLField(max_length=300)
    def __str__(self):
        return self.Product_name

class Order(models.Model):
    Client = models.ForeignKey(User, on_delete=models.CASCADE)
    Order_id = models.AutoField
    items_json = models.CharField(max_length=500)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=90)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200)
    city = models.CharField(max_length=90)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=90)
    phone = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name
