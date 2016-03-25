from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Product(models.Model):
    class Meta():
        db_table = "product"
    product_name = models.CharField(max_length=200)
    product_image = models.ImageField(default=None)
    product_type = models.CharField(default='notebook', max_length=100)
    product_description = models.TextField(default='')
    product_cost = models.IntegerField(default=0)
    product_rate = models.IntegerField(default=0)
    product_brand = models.TextField(default='')
    product_memory = models.IntegerField(default=0)
    product_orm = models.IntegerField(default=0)

class Comments(models.Model):
    class Meta():
        db_table = 'comments'

    comments_text = models.TextField()
    comments_product = models.ForeignKey(Product)
