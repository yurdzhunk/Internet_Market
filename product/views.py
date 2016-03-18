from django.shortcuts import render
from django.http.response import HttpResponse

# Create your views here.
def basic_one(request):
    first_view = 'basic one'
    html = "<html><body> This is %s view</html></body>" %first_view
    return HttpResponse(html)