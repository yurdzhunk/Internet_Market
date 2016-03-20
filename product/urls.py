from django.conf.urls import include, url

urlpatterns = [
    url(r'^1/', 'product.views.basic_one'),
    url(r'^2/', 'product.views.template_two'),
    url(r'^3/', 'product.views.template_three_simple'),
    url(r'^product/get/(?P<product_id>\d+)/$', 'product.views.product'),
    url(r'^product/addlike/(?P<product_id>\d+)/$', 'product.views.product'),
    url(r'^', 'product.views.products'),

]