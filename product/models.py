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
    product_memory = models.IntegerField(default=0)
    product_orm = models.IntegerField(default=0)
    users_liked = models.ManyToManyField(User)

    def __str__(self):              # __unicode__ on Python 2
        return self.product_name


class Basket(models.Model):
    class Meta:
        db_table = 'basket'

    chosen_products = models.CharField(default='[]', max_length=200)

    def set_list_of_products(self):
        return json.dumps(self.chosen_products)

    def get_list_of_products(self):
        return json.loads(self.chosen_products)

    def add_product(self, product_name):
        list_of_product = json.loads(self.chosen_products)
        list_of_product.append(product_name)
        self.chosen_products = json.dumps(list_of_product)

    def clean_basket(self):
        list_of_product = json.loads(self.chosen_products)
        list_of_product = []
        self.chosen_products = json.dumps(list_of_product)

class Comments(models.Model):
    class Meta():
        db_table = 'comments'

    comments_text = models.TextField()
    comments_product = models.ForeignKey(Product)
