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
    emails_username = models.CharField(max_length=200)

    def email_is_valid(self):
        if validate_email(self.email):
            return True


class IP_adress(models.Model):
    class Meta():
        db_table = 'ip_adress'

    ip = models.CharField(max_length=200)
    list_of_products = models.ManyToManyField(Product)

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
    list_of_watched_products = models.ManyToManyField(Product)

    #def get_list_of_products(self):
    #    return json.loads(self.list_of_watched_products)

    #def set_list_of_products(self):
    #    return json.dumps(self.list_of_watched_products)