from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.core.context_processors import csrf
from product.models import Basket
from loginsys.models import User_Email, Product_watched
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from loginsys.forms import UserCreateForm
from product.models import Orders, Product, FilteredProducts
from datetime import datetime
import json

@csrf_protect
def login(request):
    args = {}
    number_of_products = 0
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            if Basket.objects.filter(id=request.user.id).count() == 0:
                basket = Basket(id=request.user.id)
                basket.save()
            else:
                basket = Basket.objects.get(id=request.user.id)
                basket.clean_basket()
                basket.save()
            if FilteredProducts.objects.filter(id=request.user.id).count() == 0:
                list_of_filtered_products = FilteredProducts(id=request.user.id)
                list_of_filtered_products.save()
            else:
                list_of_filtered_products = FilteredProducts.objects.get(id=request.user.id)
                list_of_filtered_products.clean_list_of_filtered_products()
                list_of_filtered_products.save()
            if Product_watched.objects.filter(name_of_user=username).count() == 0:
                obj = Product_watched(name_of_user=username)
                obj.save()
            cost = 0
            cost = basket.get_basket_cost(cost)
            number_of_products = len(basket.get_list_of_products())
            args['number_of_products'] = number_of_products
            args['cost'] = cost
            args['username'] = username
            #return render_to_response('start_page.html', args)
            return redirect('http://127.0.0.1:8000/market/')
        else:
            args['login_error'] = 'Log in error'
            return render_to_response('login_page.html', args)
    else:
        return render_to_response('login_page.html', args)


def login_page(request):
    args = {}
    number_of_products = 0
    cost = 0
    args['cost'] = cost
    number_of_products = 0
    args['number_of_products'] = number_of_products
    args.update(csrf(request))
    return render_to_response('login_page.html', args)

def register_page(request):
    args = {}
    number_of_products = 0
    cost = 0
    args.update(csrf(request))
    args['cost'] = cost
    number_of_products = 0
    args['number_of_products'] = number_of_products
    args['form'] = UserCreateForm()
    return render_to_response('register_page.html', args)

def logout(request):
    basket = Basket.objects.get(id=request.user.id)
    basket.clean_basket()
    basket.save()
    auth.logout(request)
    return redirect('http://127.0.0.1:8000/market/')


def register(request):
    args = {}
    number_of_products = 0
    args.update(csrf(request))
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    email = request.POST.get('email', '')
    adress = request.POST.get('adress', '')
    telephone = request.POST.get('telephone', '')
    dict_of_user = {'username': [username], 'password1': [password], 'password2': [password], 'email': [email]}
    # args['form'] = UserCreationForm()

    print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA it is request.POST', request.POST)
    if request.POST:
        print('BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB, request is POST')
        newuser_form = UserCreationForm(request.POST)
        email = request.POST.get('email', '')
        new_email = User_Email(email=email)
        # newuser_form = UserCreateForm()
        # newuser_form.username = username
        # newuser_form.password1 = password
        # newuser_form.password2 = password
        # newuser_form.email = email
        # newuser_form.is_bound = True
        print('EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE', newuser_form)
        if newuser_form.is_valid() and new_email.email_is_valid():
            print('CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC')
            newuser_form.save()
            new_email.emails_username = newuser_form.cleaned_data['username']
            new_email.adress_of_user = adress
            new_email.telephone_of_user = telephone
            new_email.save()
            newuser = auth.authenticate(username=newuser_form.cleaned_data['username'],
                                        password=newuser_form.cleaned_data['password2'])
            auth.login(request, newuser)
            basket = Basket(id=request.user.id)
            basket.save()
            watched_products_object = Product_watched(name_of_user=username)
            watched_products_object.save()
            return redirect('http://127.0.0.1:8000/market/')
        else:
            print('DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD')
    return render_to_response('register_page.html', args)


def cabinet(request):
    args = {}
    cost = 0
    number_of_products = 0
    username = request.user.username
    list_of_orders = Orders.objects.filter(orders_name=request.user.username)
    list_of_list_of_product_name = []
    list_of_list_of_product = []
    list_of_product = []
    list_of_date = []
    first_date = datetime.now()
    i = 0

    for orders in list_of_orders:
        print('IIIIIIIIIIII IIIIIIIIIIIIIIII IIIIIIIIIIIIIIIII')
        list_of_list_of_product_name.append(orders.get_ordered_products())
        if i == 1:
            print('DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD', orders.date_of_order)
            list_of_date.append(orders.date_of_order)
        elif i == 0:
            print('DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD', orders.date_of_order)
            first_date = orders.date_of_order
            i = 1

    for order in list_of_list_of_product_name:
        print('IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII', order)
        for name_of_product in order:
            list_of_product.append(Product.objects.get(product_name=name_of_product))
        list_of_list_of_product.append(list_of_product)
        list_of_product = []

    args['username'] = username
    args['list_of_list_of_product'] = list_of_list_of_product
    args['len_of_list'] = len(list_of_list_of_product)
    args['list_of_date'] = list_of_date
    basket = Basket.objects.get(id=request.user.id)
    cost = basket.get_basket_cost(cost)
    number_of_products = len(basket.get_list_of_products())
    args['number_of_products'] = number_of_products
    args['cost'] = cost
    args['first_date'] = first_date


    return render_to_response('cabinet.html', args)




















