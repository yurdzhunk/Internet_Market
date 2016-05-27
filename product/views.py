from django.shortcuts import render, render_to_response, redirect
from django.http.response import HttpResponse, Http404
from django.template.loader import get_template
from django.template import Context
from product.models import Product, Comments, Basket
from django.core.exceptions import ObjectDoesNotExist
from django.core.context_processors import csrf
from product.forms import CommentForm
from django.core.paginator import Paginator
from django.contrib import auth
from django.contrib.auth.models import User


# Create your views here.
def basic_one(request):
    args = {}
    args['username'] = request.user.username
    first_view = 'basic one'
    html = "<html><body> This is %s view</html></body>" % first_view
    return render_to_response('start_page.html', args)

def company(request):
    return render_to_response('company.html')


def template_two(request):
    view = 'template_two'
    t = get_template('myview.html')
    html = t.render(Context({'name' : view}))
    return HttpResponse(html)


def template_three_simple(request):
    view = 'template_three_simple'
    return render_to_response('myview.html', {'name': view})



def products(request, page_number=1):
    args = {}
    all_products = Product.objects.all()
    current_page = Paginator(all_products, 2)
    args['products'] = current_page.page(page_number)
    args['username'] = auth.get_user(request).username
    args['path_argument'] = 2
    return render_to_response('products.html', args)


def product(request, product_id=1, comment_page_number=1):
    comment_form = CommentForm()
    args = {}
    args.update(csrf(request))
    all_comments = Comments.objects.filter(comments_product=product_id)
    current_comments = Paginator(all_comments, 4)
    args['product'] = Product.objects.get(id=product_id)
    args['comments'] = current_comments.page(comment_page_number)
    args['form'] = comment_form
    args['username'] = auth.get_user(request).username
    args['path_argument'] = 1
    return render_to_response('product.html', args)

#def addlike(request, path_argument, product_id, comment_page_number):
def addlike(request, product_id):
    username = auth.get_user(request).username
    technik = Product.objects.get(id=product_id)
    #if path_argument == '2':
    #    path = 'http://127.0.0.1:8000/page/%s/' % comment_page_number
    #if path_argument == '1':
    #    path = 'http://127.0.0.1:8000/product/get/%s/%s/' % (product_id, comment_page_number)
    try:
        user = User.objects.get(username=username)
        #print('START: user.product_set.all()', user.product_set.all())
        if username and user not in technik.users_liked.all():
            # print('user.product_set.all()', user.product_set.all())
            technik.product_rate += 1
            technik.users_liked.add(user)
            technik.save()
            #print(username)
            #print('technik not in user.product_set.all()', technik.users_liked)
            #print(len(technik.users_liked))
            #technik.save()
            #print('user.product_set.all()', user.product_set.all())
        elif username and user in technik.users_liked.all():
            technik.product_rate -= 1
            technik.users_liked.remove(user)
            technik.save()
            #print('user.product_set.all()', user.product_set.all())
            #print(username)
            #print('technik in user.product_set.all()', technik.users_liked)
            #print(len(technik.users_liked))
            #technik.save()
            #print('user.product_set.all()', user.product_set.all())
    except ObjectDoesNotExist:
        raise Http404
    return redirect('http://127.0.0.1:8000/shop/notebook/')


def add_to_basket(request, product_id):
    print('add_to_basket')
    username = auth.get_user(request).username
    technik = Product.objects.get(id=product_id)
    print('username: ', username)
    if username:
        try:
            basket = Basket.objects.get(id=request.user.id)
            if username and (technik.product_name not in basket.get_list_of_products()):
                basket.add_product(technik.product_name)
                basket.save()
        except ObjectDoesNotExist:
            raise Http404
        return redirect('http://127.0.0.1:8000/shop/notebook/')


def addcomment(request, product_id):
    if request.POST and ('bla' not in request.session):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.comments_product = Product.objects.get(id=product_id)
            form.save()
            request.session.set_expiry(60)
            request.session['bla'] = True
    return redirect('http://127.0.0.1:8000/product/get/%s/' % product_id)


def market(request):
    args = {}
    return render_to_response('shop.html', {})


def startpage(request):
    args = {}
    args['username'] = auth.get_user(request).username
    return render_to_response('start_page.html', args)


def notebook(request):
    args = {}
    args['username'] = request.user.username
    args['techniks'] = Product.objects.filter(product_type='notebook')
    args['img1'] = args['techniks'][0].product_image.url
    print(args['img1'])
    return render_to_response('shop.html', args)


def smartphone(request):
    args = {}
    args['techniks'] = Product.objects.filter(product_type='smartphone')
    return render_to_response('shop.html', args)


def tv(request):
    args = {}
    args['techniks'] = Product.objects.filter(product_type='tv')
    return render_to_response('shop.html', args)

def product_page(request, product_id):
    args = {}
    technik = Product.objects.get(id=product_id)
    args['product'] = technik
    return render_to_response('product_page.html', args)


