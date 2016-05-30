from django.contrib import admin
from product.models import Product, Comments, Orders

# Register your models here.
class ArticleInline(admin.StackedInline):
    model = Comments
    extra = 2


class ProductAdmin(admin.ModelAdmin):
    fields = ['product_brand', 'product_name', 'product_type', 'product_image', 'product_description', 'product_cost',
              'product_screen_resolution', 'product_memory', 'product_orm']
    inlines = [ArticleInline]
    list_filter = ['product_name']


admin.site.register(Product, ProductAdmin)


class OrderAdmin(admin.ModelAdmin):
    fields = ['ordered_products', 'orders_cost', 'adress_of_orderer', 'orders_name', 'orders_phone_number']
    list_filter = ['orders_name']


admin.site.register(Orders, OrderAdmin)
