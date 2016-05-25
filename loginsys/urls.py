from django.conf.urls import include, url

urlpatterns = [

    url(r'^logout/', 'loginsys.views.logout'),
    url(r'^login/', 'loginsys.views.login'),
    url(r'^login_page/', 'loginsys.views.login_page'),
    url(r'^register/', 'loginsys.views.register'),
    url(r'^register_page/', 'loginsys.views.register_page'),



]

