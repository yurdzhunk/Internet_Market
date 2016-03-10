from django.conf.urls import include, url

urlpatterns = [
    url(r'^', 'market.views.start_page'),
]