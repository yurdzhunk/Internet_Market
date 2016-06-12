#coding=<encoding name>
from django.shortcuts import render, render_to_response, redirect
from django.http.response import HttpResponse, Http404
from django.template.loader import get_template
from django.template import Context
from product.models import Product, Comments, Basket, Orders, FilteredProducts
from django.core.exceptions import ObjectDoesNotExist
from django.core.context_processors import csrf
from product.forms import CommentForm
from django.core.paginator import Paginator
from django.contrib import auth
from django.contrib.auth.models import User
from datetime import datetime
from django.views.decorators.csrf import csrf_protect
from loginsys.models import Product_watched, IP_adress
from django.db.models import Q

# Create your views here.
def basic_one(request):
    args = {}
    username = request.user.username
    cost = 0
    if username:
        basket  = Basket.objects.get(id=request.user.id)
        cost = basket.get_basket_cost(cost)
    args['cost'] = cost
    args['username'] = username
    list1 = []
    list2 = []
    ip_object = IP_adress()
    ip = ip_object.get_client_ip(request)
    if username:
        user_object = Product_watched.objects.get(name_of_user=username)
        list_of_products = user_object.get_list_of_products()
        args['len'] = len(list_of_products)
    else:
        ip_object = IP_adress.objects.get(ip=ip)
        list_of_products = ip_object.get_list_of_products()
        args['len'] = len(list_of_products)
    print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', len(list_of_products))
    if 4 <= args['len'] < 8:
        print('BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB')
        for i in range(len(list_of_products)-4, len(list_of_products)):
            prod = Product.objects.get(product_name=list_of_products[i])
            list1.append(prod)
        args['list1'] = list1
        return render_to_response('start_page.html', args)
    elif args['len'] == 8:
        print('CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC')
        for i in range(4):
            prod = Product.objects.get(product_name=list_of_products[i])
            list1.append(prod)
        for i in range(4, 8):
            prod = Product.objects.get(product_name=list_of_products[i])
            list2.append(prod)
        args['list1'] = list1
        args['list2'] = list2
        return render_to_response('start_page.html', args)
    return render_to_response('start_page.html', args)


def company(request):
    args = {}
    username = request.user.username
    cost = 0
    if username:
        basket = Basket.objects.get(id=request.user.id)
        cost = basket.get_basket_cost(cost)
    args['cost'] = cost
    args['username'] = username
    return render_to_response('company.html', args)


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
    return redirect('http://127.0.0.1:8000/shop/notebook/1/0/')


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
        if technik.product_type == 'notebook':
            return redirect('http://127.0.0.1:8000/shop/notebook/')
        elif technik.product_type == 'smartphone':
            return redirect('http://127.0.0.1:8000/shop/smartphone/')
        elif technik.product_type == 'tv':
            return redirect('http://127.0.0.1:8000/shop/tv/')

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
    username = auth.get_user(request).username
    args['username'] = username
    ip_object = IP_adress()
    ip = IP_adress.get_client_ip(request)
    if username:
        user_object = Product_watched.objects.get(name_of_user=username)
        list_products_of_user = user_object.list_of_watched_products
        args['list_products_of_user'] = list_products_of_user
    else:
        ip_object = IP_adress.objects.get(ip=ip)
        list_products_of_ip = ip_object.list_of_products
        args['list_products_of_ip'] = list_products_of_ip
    return render_to_response('start_page.html', args)


@csrf_protect
def notebook(request, page_number=1, filtring=0):
    filtring = filtring
    old_filter = True
    args = {}
    args.update(csrf(request))
    username = request.user.username
    cost = 0
    if username:
        basket = Basket.objects.get(id=request.user.id)
        cost = basket.get_basket_cost(cost)
    all_products = Product.objects.filter(product_type='notebook')
    current_products = Paginator(all_products, 6)
    args['cost'] = cost
    args['username'] = username
    args['type'] = 'notebook'
    print('FILTRING ===========================================', filtring)
    print('PAGE NUMBER ===========================================', page_number)
    if request.POST or filtring == '1':
        print('WORKING IN if request.POST or filtring == 1')
        if filtring != '1':
            page_number = 1
        apple = request.POST.get('apple', '')
        asus = request.POST.get('asus', '')
        samsung = request.POST.get('samsung', '')
        acer = request.POST.get('acer', '')
        lenovo = request.POST.get('lenovo', '')
        dell = request.POST.get('dell', '')
        hp = request.POST.get('hp', '')
        if (apple=='') and (asus=='') and (samsung=='') and (acer=='') and (lenovo=='') and (dell=='') and (hp=='') and request.POST:
            apple='Apple' 
            asus='ASUS' 
            samsung='Samsung' 
            acer='ACER' 
            lenovo='Lenovo' 
            dell='Dell' 
            hp='HP'
            old_filter = False
        res1 = request.POST.get('screen_resol_1', '')
        res2 = request.POST.get('screen_resol_2', '')
        res3 = request.POST.get('screen_resol_3', '')
        if res1=='' and res2=='' and res3=='' and request.POST:
            res1="15.2''" 
            res2="15.4''" 
            res3="15.6''"
            old_filter = False
        some_prod = Product.objects.get(id=1)
        print('APPLE MEMORYYYYYYYYYYYYYYYYY ', some_prod.product_orm)
        orm_size1 = request.POST.get('orm_size1', '')
        orm_size2 = request.POST.get('orm_size2', '')
        orm_size3 = request.POST.get('orm_size3', '') 
        print('MEMORY SIZEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE', orm_size1)
        print('MEMORY SIZEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE', orm_size2)
        if orm_size1=='' and orm_size2=='' and orm_size3=='' and request.POST:
            orm_size1 = '4 GB'
            orm_size2 = '16 GB'
            orm_size3 = '8 GB'
            old_filter = False
        memory_size1 = request.POST.get('512-HDD', '')
        memory_size2 = request.POST.get('512-SSD', '')
        memory_size3 = request.POST.get('1TB', '')
        if memory_size1=='' and memory_size2=='' and memory_size3=='' and request.POST:
            memory_size1 = '512 GB SSD'
            memory_size2 = '512 GB HDD'
            memory_size3 = '1 TB'
            old_filter = False

        filtered_products = list(Product.objects.filter(Q(product_brand=apple) | Q(product_brand=asus) | Q(product_brand=samsung) |
                                                        Q(product_brand=acer) | Q(product_brand=lenovo) | Q(product_brand=dell)  |
                                                        Q(product_brand=hp), Q(product_screen_resolution=res1) | Q(product_screen_resolution=res2) |
                                                        Q(product_screen_resolution=res3), Q(product_orm=orm_size1) | Q(product_orm=orm_size2) | Q(product_orm=orm_size3),
                                                        Q(product_memory=memory_size1) | Q(product_memory=memory_size2) |
                                                        Q(product_memory=memory_size3),
                                                         product_type='notebook'))
        print('_FILTER_FILTER_FILTER_FILTER_FILTER_FILTER_FILTER ', filtered_products)
        print('OLD FILTER =============================================', old_filter)
        if not old_filter:
            print('CREATING LIST OF FILTERED PRODUCTS!!!!!!!!!!!!!!!!!!!!!!!!!')
            if username:
                list_of_filtered_products = FilteredProducts(id=request.user.id)
                list_of_filtered_products.save()
            else:
                filtered_products_object = FilteredProducts()
                ip_of_user = filtered_products_object.get_client_ip(request)
                if FilteredProducts.objects.filter(ip_of_user=ip_of_user).count() == 0:
                    list_of_filtered_products = FilteredProducts(ip_of_user=ip_of_user)
                    list_of_filtered_products.save()
                else:
                    list_of_filtered_products = FilteredProducts.objects.get(ip_of_user=ip_of_user)

        #if not old_filter:
            list_of_filtered_products.clean_list_of_filtered_products()
            for product in filtered_products:
                list_of_filtered_products.add_product(product.product_name)
            list_of_filtered_products.save()
            #####
        paginator_filtered_products = Paginator(filtered_products, 6)
        filtring = 1
        args['filtring'] = filtring
        if old_filter:
            print('WE USE OLD FILTER!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            if username:
                list_of_filtered_products_name = FilteredProducts.objects.get(id=request.user.id).get_list_of_products()
            else:
                filtered_products_object = FilteredProducts()
                ip_of_user = filtered_products_object.get_client_ip(request)
                list_of_filtered_products_name = FilteredProducts.objects.get(ip_of_user=ip_of_user).get_list_of_products()
            list_of_filtered_products = []
            for product_name in list_of_filtered_products_name:
                list_of_filtered_products.append(Product.objects.get(product_name=product_name))
            paginator_filtered_products = Paginator(list_of_filtered_products, 6)
        print('PAGE NUMBER ===========================================', page_number)
        args['techniks'] = paginator_filtered_products.page(page_number)
        return render_to_response('shop.html', args)
    args['filtring'] = filtring
    args['techniks'] = current_products.page(page_number)
    #args['img1'] = args['techniks'][0].product_image.url
    #print(args['img1'])
    return render_to_response('shop.html', args)


def smartphone(request, page_number=1, filtring=0):
    args = {}
    args.update(csrf(request))
    old_filter = True
    username = request.user.username
    cost = 0
    args['username'] = request.user.username
    if username:
        basket = Basket.objects.get(id=request.user.id)
        cost = basket.get_basket_cost(cost)
    all_products = Product.objects.filter(product_type='smartphone')
    current_products = Paginator(all_products, 6)
    args['cost'] = cost
    args['techniks'] = current_products.page(page_number)
    args['type'] = 'smartphone'
    print('FILTRING ===========================================', filtring)
    print('PAGE NUMBER ===========================================', page_number)
    if request.POST or filtring == '1':
        print('WORKING IN if request.POST or filtring == 1')
        if filtring != '1':
            page_number = 1
        apple = request.POST.get('apple', '')
        samsung = request.POST.get('samsung', '')
        motorola = request.POST.get('motorola', '')
        microsoft = request.POST.get('microsoft', '')
        lenovo = request.POST.get('lenovo', '')
        lg = request.POST.get('lg', '')
        if (samsung=='') and (microsoft=='') and (apple=='') and (motorola=='') and (lenovo=='') and (lg=='') and request.POST:
            samsung='Samsung' 
            microsoft='Microsoft' 
            lg='LG' 
            lenovo='Lenovo' 
            apple='Apple' 
            motorola='Motorola' 
            old_filter = False
        res1 = request.POST.get('screen_resol_1', '')
        res2 = request.POST.get('screen_resol_2', '')
        res3 = request.POST.get('screen_resol_3', '')
        res4 = request.POST.get('screen_resol_4', '')
        res5 = request.POST.get('screen_resol_5', '')
        if res1=='' and res2=='' and res3=='' and res4=='' and res5=='' and request.POST:
            res1="4.7''" 
            res2="5.2''" 
            res3="5.4''"
            res4="5.5''"
            res5="5.7''"
            old_filter = False
        some_prod = Product.objects.get(id=1)
        print('APPLE MEMORYYYYYYYYYYYYYYYYY ', some_prod.product_orm)
        orm_size1 = request.POST.get('orm_size1', '')
        orm_size2 = request.POST.get('orm_size2', '')
        orm_size3 = request.POST.get('orm_size3', '') 
        orm_size4 = request.POST.get('orm_size4', '') 
        print('MEMORY SIZEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE', orm_size1)
        print('MEMORY SIZEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE', orm_size2)
        if orm_size1=='' and orm_size2=='' and orm_size3=='' and orm_size4=='' and request.POST:
            orm_size1 = '1 GB'
            orm_size2 = '2 GB'
            orm_size3 = '3 GB'
            orm_size4 = '4 GB'
            old_filter = False
        memory_size1 = request.POST.get('16 GB', '')
        memory_size2 = request.POST.get('32 GB', '')
        memory_size3 = request.POST.get('2TB', '')
        if memory_size1=='' and memory_size2=='' and memory_size3=='' and request.POST:
            memory_size1 = '16 GB'
            memory_size2 = '32 GB'
            memory_size3 = '2 TB'
            old_filter = False

        filtered_products = list(Product.objects.filter(Q(product_brand=samsung) | Q(product_brand=motorola) | Q(product_brand=lg) |
                                                        Q(product_brand=apple) | Q(product_brand=microsoft) | Q(product_brand=lenovo), Q(product_screen_resolution=res1) | Q(product_screen_resolution=res2) |
                                                        Q(product_screen_resolution=res3) | Q(product_screen_resolution=res4) | Q(product_screen_resolution=res5),
                                                        Q(product_orm=orm_size1) | Q(product_orm=orm_size2) | Q(product_orm=orm_size3) | Q(product_orm=orm_size4),
                                                        Q(product_memory=memory_size1) | Q(product_memory=memory_size2) |
                                                        Q(product_memory=memory_size3),
                                                         product_type='smartphone'))
        print('_FILTER_FILTER_FILTER_FILTER_FILTER_FILTER_FILTER ', filtered_products)
        print('OLD FILTER =============================================', old_filter)
        if not old_filter:
            print('CREATING LIST OF FILTERED PRODUCTS!!!!!!!!!!!!!!!!!!!!!!!!!')
            if username:
                list_of_filtered_products = FilteredProducts(id=request.user.id)
                list_of_filtered_products.save()
            else:
                filtered_products_object = FilteredProducts()
                ip_of_user = filtered_products_object.get_client_ip(request)
                if FilteredProducts.objects.filter(ip_of_user=ip_of_user).count() == 0:
                    list_of_filtered_products = FilteredProducts(ip_of_user=ip_of_user)
                    list_of_filtered_products.save()
                else:
                    list_of_filtered_products = FilteredProducts.objects.get(ip_of_user=ip_of_user)

        #if not old_filter:
            list_of_filtered_products.clean_list_of_filtered_products()
            for product in filtered_products:
                list_of_filtered_products.add_product(product.product_name)
            list_of_filtered_products.save()
            #####
        paginator_filtered_products = Paginator(filtered_products, 6)
        filtring = 1
        args['filtring'] = filtring
        if old_filter:
            print('WE USE OLD FILTER!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            if username:
                list_of_filtered_products_name = FilteredProducts.objects.get(id=request.user.id).get_list_of_products()
            else:
                filtered_products_object = FilteredProducts()
                ip_of_user = filtered_products_object.get_client_ip(request)
                list_of_filtered_products_name = FilteredProducts.objects.get(ip_of_user=ip_of_user).get_list_of_products()
            list_of_filtered_products = []
            for product_name in list_of_filtered_products_name:
                list_of_filtered_products.append(Product.objects.get(product_name=product_name))
            paginator_filtered_products = Paginator(list_of_filtered_products, 6)
        print('PAGE NUMBER ===========================================', page_number)
        args['techniks'] = paginator_filtered_products.page(page_number)
        return render_to_response('shop.html', args)
    args['filtring'] = filtring
    args['techniks'] = current_products.page(page_number)
    #args['img1'] = args['techniks'][0].product_image.url
    #print(args['img1'])
    return render_to_response('shop.html', args)


def tv(request, page_number=1, filtring=0):
    args = {}
    args.update(csrf(request))
    old_filter = True
    username = request.user.username
    cost = 0
    args['username'] = request.user.username
    if username:
        basket = Basket.objects.get(id=request.user.id)
        cost = basket.get_basket_cost(cost)
    all_products = Product.objects.filter(product_type='tv')
    current_products = Paginator(all_products, 6)
    args['cost'] = cost
    args['techniks'] = current_products.page(page_number)
    args['type'] = 'tv'
    print('FILTRING ===========================================', filtring)
    print('PAGE NUMBER ===========================================', page_number)
    if request.POST or filtring == '1':
        print('WORKING IN if request.POST or filtring == 1')
        if filtring != '1':
            page_number = 1
        sony = request.POST.get('sony', '')
        samsung = request.POST.get('samsung', '')
        lg = request.POST.get('lg', '')
        philips = request.POST.get('philips', '')
        if (sony=='') and (samsung=='') and (lg=='') and (philips=='') and request.POST:
            sony='Sony' 
            samsung='Samsung' 
            lg='LG' 
            philips='Philips' 
            old_filter = False
        res1 = request.POST.get('screen_resol_1', '')
        res2 = request.POST.get('screen_resol_2', '')
        res3 = request.POST.get('screen_resol_3', '')
        res4 = request.POST.get('screen_resol_4', '')
        if res1=='' and res2=='' and res3=='' and res4=='' and request.POST:
            res1="40''" 
            res2="43''" 
            res3="50''"
            res4="84''"
            old_filter = False
        some_prod = Product.objects.get(id=1)

        filtered_products = list(Product.objects.filter(Q(product_brand=sony) | Q(product_brand=samsung) | Q(product_brand=lg) |
                                                        Q(product_brand=philips), Q(product_screen_resolution=res1) | Q(product_screen_resolution=res2) |
                                                        Q(product_screen_resolution=res3) | Q(product_screen_resolution=res4),
                                                         product_type='tv'))
        print('_FILTER_FILTER_FILTER_FILTER_FILTER_FILTER_FILTER ', filtered_products)
        print('OLD FILTER =============================================', old_filter)
        if not old_filter:
            print('CREATING LIST OF FILTERED PRODUCTS!!!!!!!!!!!!!!!!!!!!!!!!!')
            if username:
                list_of_filtered_products = FilteredProducts(id=request.user.id)
                list_of_filtered_products.save()
            else:
                filtered_products_object = FilteredProducts()
                ip_of_user = filtered_products_object.get_client_ip(request)
                if FilteredProducts.objects.filter(ip_of_user=ip_of_user).count() == 0:
                    list_of_filtered_products = FilteredProducts(ip_of_user=ip_of_user)
                    list_of_filtered_products.save()
                else:
                    list_of_filtered_products = FilteredProducts.objects.get(ip_of_user=ip_of_user)

        #if not old_filter:
            list_of_filtered_products.clean_list_of_filtered_products()
            for product in filtered_products:
                list_of_filtered_products.add_product(product.product_name)
            list_of_filtered_products.save()
            #####
        paginator_filtered_products = Paginator(filtered_products, 6)
        filtring = 1
        args['filtring'] = filtring
        if old_filter:
            print('WE USE OLD FILTER!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            if username:
                list_of_filtered_products_name = FilteredProducts.objects.get(id=request.user.id).get_list_of_products()
            else:
                filtered_products_object = FilteredProducts()
                ip_of_user = filtered_products_object.get_client_ip(request)
                list_of_filtered_products_name = FilteredProducts.objects.get(ip_of_user=ip_of_user).get_list_of_products()
            list_of_filtered_products = []
            for product_name in list_of_filtered_products_name:
                list_of_filtered_products.append(Product.objects.get(product_name=product_name))
            paginator_filtered_products = Paginator(list_of_filtered_products, 6)
        print('PAGE NUMBER ===========================================', page_number)
        args['techniks'] = paginator_filtered_products.page(page_number)
        return render_to_response('shop.html', args)
    args['filtring'] = filtring
    return render_to_response('shop.html', args)


def notebook_product_page(request, product_id):
    args = {}
    username = request.user.username
    cost = 0
    prod = Product.objects.get(id=product_id)
    if username:
        basket = Basket.objects.get(id=request.user.id)
        cost = basket.get_basket_cost(cost)
        #bla = Product_watched.objects.get(name_of_user=username)
        #print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA   ', len(bla.get_list_of_products()))
        if len(Product_watched.objects.filter(name_of_user=username)) == 0:
            print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA   ', username)
            print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA   ', Product_watched.objects.filter(name_of_user=username))
            watched_prod = Product_watched(name_of_user=username)
        else:
            watched_prod = Product_watched.objects.get(name_of_user=username)
            print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA   ', Product_watched.objects.filter(name_of_user=username))
            print('BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB   ', watched_prod.list_of_watched_products)
        #list_of_watched_products = watched_prod.get_list_of_products()
        #list_of_watched_products.append(prod.product_name)
        #watched_prod.list_of_watched_products = list_of_watched_products
        watched_prod.add_product(prod.product_name)
        watched_prod.save()
    else:
        current_ip_object = IP_adress()
        ip = current_ip_object.get_client_ip(request)
        if len(IP_adress.objects.filter(ip=ip)) == 0:
            current_ip_object.ip = ip
            current_ip_object.save()
        else:
            current_ip_object = IP_adress.objects.get(ip=ip)
        current_ip_object.add_product(prod.product_name)
        current_ip_object.save()
    args['cost'] = cost
    technik = Product.objects.get(id=product_id)
    args['product'] = technik
    args['username'] = username
    return render_to_response('notebook_product_page.html', args)


def basket(request, flag_adress=True, flag_phone=True, adress='', phone=''):
    args = {}
    args['flag_adress'] = flag_adress
    args['flag_phone'] = flag_phone
    args['adress_default'] = adress
    args['phone_default'] = phone
    args.update(csrf(request))
    username = request.user.username
    cost = 0
    basket = Basket.objects.get(id=request.user.id)
    cost = basket.get_basket_cost(cost)
    args['cost'] = cost
    print('CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC', basket.chosen_products)
    list_of_products_name = basket.get_list_of_products()
    list_of_products = []
    for product_name in list_of_products_name:
        list_of_products.append(Product.objects.get(product_name=product_name))
    args['length'] = len(list_of_products)
    args['list_of_products'] = list_of_products
    args['username'] = request.user.username
    return render_to_response('basket.html', args)


def booking(request):
    username = request.user.username
    cost = 0
    adress = request.POST.get('adress', '')
    phone_number = request.POST.get('phone', '')
    if adress != '' and phone_number != '':
        basket1 = Basket.objects.get(id=request.user.id)
        cost = basket1.get_basket_cost(cost)
        order = Orders(orders_name=username)
        order.ordered_products = basket1.chosen_products
        order.adress_of_orderer = adress
        order.orders_phone_number = phone_number
        order.orders_cost = cost
        order.date_of_order = datetime.now()
        basket1.clean_basket()
        basket1.save()
        order.save()
        args = {}
        args['username'] = username
        args['cost'] = 0
        return render_to_response('readyorder.html', args)
    elif adress != '' and phone_number == '':
        flag_adress = True
        flag_phone = False
        return basket(request, flag_adress=flag_adress, flag_phone=flag_phone, adress=adress)
    elif adress == '' and phone_number != '':
        flag_adress = False
        flag_phone = True
        return basket(request, flag_adress=flag_adress, flag_phone=flag_phone, phone=phone_number)
    elif adress == '' and phone_number == '':
        flag_adress = False
        flag_phone = False
        return basket(request, flag_adress=flag_adress, flag_phone=flag_phone)


def delete_product(request, product_id):
    user_id = request.user.id
    product = Product.objects.get(id=product_id)
    basket = Basket.objects.get(id=user_id)
    list_of_product = basket.get_list_of_products()
    print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', list_of_product)
    print('BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB', product.product_name)
    basket.delete_product(product.product_name)
    basket.save()
    return redirect('http://127.0.0.1:8000/basket/')

def ready_order(request):
    args = {}
    args['username'] = request.user.username
    return render_to_response('readyorder.html', args)

def akcii(request):
    args = {}
    args['username'] = request.user.username
    return render_to_response('akcii.html', args)

def contacts(request):
    args = {}
    args['username'] = request.user.username
    return render_to_response('contacts.html', args)



