from django.conf.urls import include, url

urlpatterns = [
    url(r'^1/', 'product.views.basic_one'),
    url(r'^2/', 'product.views.template_two'),
    url(r'^3/', 'product.views.template_three_simple'),
    url(r'^product/get/(?P<product_id>\d+)/$', 'product.views.product'),

    url(r'^product/get/(?P<product_id>\d+)/(?P<comment_page_number>\d+)/$', 'product.views.product'),
    url(r'^product/addlike/(?P<path_argument>\d+)/(?P<product_id>\d+)/(?P<comment_page_number>\d+)/$', 'product.views.addlike'),
    url(r'^product/addcomment/(?P<product_id>\d+)/$', 'product.views.addcomment'),
    url(r'^page/(\d+)/$', 'product.views.products'),
    url(r'^', 'product.views.products'),

]

