from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.core.context_processors import csrf
from product.models import Basket
from loginsys.models import User_Email
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from loginsys.forms import UserCreateForm
from product.models import Orders, Product
import json

@csrf_protect
def login(request):
    args = {}
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
            cost = 0
            cost = basket.get_basket_cost(cost)
            args['cost'] = cost
            args['username'] = username
            return render_to_response('start_page.html', args)
        else:
            args['login_error'] = 'Log in error'
            return render_to_response('login_page.html', args)
    else:
        return render_to_response('login_page.html', args)


def login_page(request):
    args = {}
    cost = 0
    args['cost'] = cost
    args.update(csrf(request))
    return render_to_response('login_page.html', args)

def register_page(request):
    args = {}
    cost = 0
    args.update(csrf(request))
    args['cost'] = cost
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
    args.update(csrf(request))
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    email = request.POST.get('email', '')
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
            new_email.save()
            newuser = auth.authenticate(username=newuser_form.cleaned_data['username'],
                                        password=newuser_form.cleaned_data['password2'])
            auth.login(request, newuser)
            basket = Basket(id=request.user.id)
            basket.save()
            return redirect('http://127.0.0.1:8000/1/')
        else:
            print('DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD')
    return render_to_response('register_page.html', args)


def cabinet(request):
    args = {}
    username = request.user.username
    list_of_orders = Orders.objects.filter(orders_name=request.user.username)
    list_of_list_of_product_name = []
    list_of_list_of_product = []
    list_of_product = []

    for orders in list_of_orders:
        list_of_list_of_product_name.append(orders.get_ordered_products())

    for order in list_of_list_of_product_name:
        print('IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII', order)
        for name_of_product in order:
            list_of_product.append(Product.objects.get(product_name=name_of_product))
        list_of_list_of_product.append(list_of_product)
        list_of_product = []

    args['username'] = username
    args['list_of_list_of_product'] = list_of_list_of_product
    args['len_of_list'] = len(list_of_list_of_product)


    return render_to_response('cabinet.html', args)




















