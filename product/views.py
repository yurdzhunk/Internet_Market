from django.shortcuts import render, render_to_response
from django.http.response import HttpResponse
from django.template.loader import get_template
from django.template import Context
from product.models import Product, Comments

# Create your views here.
def basic_one(request):
    first_view = 'basic one'
    html = "<html><body> This is %s view</html></body>" % first_view
    return render_to_response('start_page.html')


def template_two(request):
    view = 'template_two'
    t = get_template('myview.html')
    html = t.render(Context({'name' : view}))
    return HttpResponse(html)


def template_three_simple(request):
    view = 'template_three_simple'
    return render_to_response('myview.html', {'name': view})


def products(request):
    products = Product.objects.all()
    return render_to_response('products.html', {'products': products})


def product(request, product_id=1):
    product_to_get = Product.objects.get(id=product_id)
    comments = Comments.objects.filter(comments_product=product_id)
    return render_to_response('product.html', {'product': product_to_get, 'comments': comments})










