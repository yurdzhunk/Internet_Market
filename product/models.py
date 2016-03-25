from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Product(models.Model):
    class Meta():
        db_table = "product"
    product_name = models.CharField(max_length=200)
    product_image = models.ImageField()
    product_description = models.TextField()
    product_cost = models.IntegerField(default=0)
    product_rate = models.IntegerField(default=0)
    product_brend = models.TextField()
    product_memory = models.IntegerField(default=0)
    product_orm = models.IntegerField(default=0)

class Comments(models.Model):
    class Meta():
        db_table = 'comments'

    comments_text = models.TextField()
    comments_product = models.ForeignKey(Product)
