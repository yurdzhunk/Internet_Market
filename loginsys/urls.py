from django.conf.urls import include, url

urlpatterns = [

    url(r'^logout/', 'loginsys.views.logout'),
    url(r'^login/', 'loginsys.views.login'),
    url(r'^register/', 'loginsys.views.register'),


]

