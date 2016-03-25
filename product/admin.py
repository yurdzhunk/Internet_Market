from django.contrib import admin
from product.models import Product, Comments

# Register your models here.
class ArticleInline(admin.StackedInline):
    model = Comments
    extra = 2


class ProductAdmin(admin.ModelAdmin):
    fields = ['product_brand', 'product_name', 'product_type', 'product_image', 'product_description', 'product_cost']
    inlines = [ArticleInline]
    list_filter = ['product_name']


admin.site.register(Product, ProductAdmin)
