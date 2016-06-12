from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^market/', 'product.views.basic_one'),
    url(r'^2/', 'product.views.template_two'),
    url(r'^3/', 'product.views.template_three_simple'),
    url(r'^basket/', 'product.views.basket'),
    url(r'^booking/', 'product.views.booking'),
    url(r'^delete/(?P<product_id>\d+)/$', 'product.views.delete_product'),
    url(r'^product/get/(?P<product_id>\d+)/$', 'product.views.product'),
    url(r'^product/get/(?P<product_id>\d+)/(?P<comment_page_number>\d+)/$', 'product.views.product'),
    url(r'^product/addlike/(?P<path_argument>\d+)/(?P<product_id>\d+)/(?P<comment_page_number>\d+)/$', 'product.views.addlike'),
    url(r'^product/addcomment/(?P<product_id>\d+)/$', 'product.views.addcomment'),
    url(r'^market/$', 'product.views.market'),
    url(r'^shop/notebook/(?P<page_number>\d+)/(?P<filtring>\d+)/$', 'product.views.notebook'),
    url(r'^shop/smartphone/(?P<page_number>\d+)/(?P<filtring>\d+)/$', 'product.views.smartphone'),
    url(r'^shop/tv/(?P<page_number>\d+)/(?P<filtring>\d+)/$', 'product.views.tv'),
    url(r'^company/$', 'product.views.company'),
    url(r'^akcii/$', 'product.views.akcii'),
    url(r'^contacts/$', 'product.views.contacts'),
    url(r'^add_to_basket/(?P<product_id>\d+)/(?P<page_number>\d+)/(?P<filtring>\d+)/$', 'product.views.add_to_basket'),
    url(r'^addlike/(?P<product_id>\d+)/$', 'product.views.addlike'),
    url(r'^notebook/prod/(?P<product_id>\d+)/$', 'product.views.notebook_product_page'),
    url(r'^minus_count/(?P<product_id>\d+)/$', 'product.views.minus_count'),
    url(r'^plus_count/(?P<product_id>\d+)/$', 'product.views.plus_count'),
    url(r'^', 'product.views.products'),

]

