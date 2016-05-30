from __future__ import unicode_literals


from django.db import models
from django.contrib.auth.models import User

import json

# Create your models here.
class Product(models.Model):
    class Meta:
        db_table = "product"


    product_name = models.CharField(max_length=200)
    product_image = models.ImageField(upload_to='static')
    product_type = models.CharField(default='notebook', max_length=100)
    product_description = models.TextField(default='')
    product_cost = models.IntegerField(default=0)
    product_rate = models.IntegerField(default=0)
    product_brand = models.TextField(default='')
    product_screen_resolution = models.CharField(max_length=20)
    product_memory = models.CharField(max_length=20)
    product_orm = models.CharField(max_length=20)
    users_liked = models.ManyToManyField(User)

    def __str__(self):              # __unicode__ on Python 2
        return self.product_name


class Basket(models.Model):
    class Meta:
        db_table = 'basket'

    chosen_products = models.CharField(default='[]', max_length=200)

    def set_list_of_products(self):
        return json.dumps(self.chosen_products)

    def get_basket_cost(self, cost):
        list_of_products = self.get_list_of_products()
        for name_of_product in list_of_products:
            technik = Product.objects.get(product_name=name_of_product)
            cost += technik.product_cost
        return cost

    def get_list_of_products(self):
        return json.loads(self.chosen_products)

    def add_product(self, product_name):
        list_of_product = json.loads(self.chosen_products)
        list_of_product.append(product_name)
        self.chosen_products = json.dumps(list_of_product)

    def delete_product(self, product_name):
        list_of_product = json.loads(self.chosen_products)
        list_of_product.remove(product_name)
        self.chosen_products = json.dumps(list_of_product)

    def clean_basket(self):
        list_of_product = json.loads(self.chosen_products)
        list_of_product = []
        self.chosen_products = json.dumps(list_of_product)


class Orders(models.Model):
    class Meta():
        db_table = 'orders'

    ordered_products = models.CharField(max_length=200)
    orders_cost = models.IntegerField(default=0)
    adress_of_orderer = models.CharField(max_length=200)
    orders_name = models.CharField(max_length=200)
    orders_phone_number = models.CharField(max_length=100, default=3254362364)

    def get_ordered_products(self):
        return json.loads(self.ordered_products)


class Comments(models.Model):
    class Meta():
        db_table = 'comments'

    comments_text = models.TextField()
    comments_product = models.ForeignKey(Product)
