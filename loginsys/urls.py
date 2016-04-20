from django.conf.urls import include, url

urlpatterns = [

    url(r'^logout/', 'loginsys.views.logout'),
    url(r'^login_page/', 'loginsys.views.login_page'),
    url(r'^login/', 'loginsys.views.login'),
    url(r'^register_page/', 'loginsys.views.register'),



]

