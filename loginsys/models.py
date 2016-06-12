from __future__ import unicode_literals
from validate_email import validate_email
from django.db import models
from product.models import Product
import json


# Create your models here.

class User_Email(models.Model):

    class Meta:
        db_table = 'user_email'

    email = models.EmailField(default='test@gmail.com')
    adress_of_user = models.CharField(default='', max_length=200)
    emails_username = models.CharField(max_length=200)

    def email_is_valid(self):
        if validate_email(self.email):
            return True


class IP_adress(models.Model):
    class Meta():
        db_table = 'ip_adress'

    ip = models.CharField(max_length=200)
    list_of_products = models.CharField(default='[]', max_length=1000)

    def set_list_of_products(self):
        return json.dumps(self.list_of_products)

    def get_list_of_products(self):
        return json.loads(self.list_of_products)

    def add_product(self, product_name):
        list_of_product = json.loads(self.list_of_products)
        if len(list_of_product) < 8 and (product_name not in list_of_product):
            list_of_product.append(product_name)
        elif (product_name not in list_of_product):
            list_of_product.pop(0)
            list_of_product.append(product_name)
        self.list_of_products = json.dumps(list_of_product)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class Product_watched(models.Model):
    class Meta():
        db_table = 'watched_product'

    name_of_user = models.CharField(max_length=200)
    list_of_watched_products = models.CharField(default='[]', max_length=1000)

    def set_list_of_products(self):
        return json.dumps(self.list_of_watched_products)

    def get_list_of_products(self):
        return json.loads(self.list_of_watched_products)

    def add_product(self, product_name):
        list_of_product = json.loads(self.list_of_watched_products)
        if len(list_of_product) < 8 and (product_name not in list_of_product):
            list_of_product.append(product_name)
        elif (product_name not in list_of_product):
            list_of_product.pop(0)
            list_of_product.append(product_name)
        self.list_of_watched_products = json.dumps(list_of_product)
    #def get_list_of_products(self):
    #    return json.loads(self.list_of_watched_products)

    #def set_list_of_products(self):
    #    return json.dumps(self.list_of_watched_products)