from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.core.context_processors import csrf
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect

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
            args['username'] = username
            return render_to_response('start_page.html', args)
        else:
            args['login_error'] = 'Log in error'
            return render_to_response('login.html', args)
    else:
        return render_to_response('login_page.html', args)


def login_page(request):
    args = {}
    args.update(csrf(request))
    return render_to_response('login_page.html', args)

def register_page(request):
    return render_to_response('register_page.html', {})

def logout(request):
    auth.logout(request)
    return redirect('http://127.0.0.1:8000/1/')


def register(request):
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    if request.POST:
        newuser_form = UserCreationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(username=newuser_form.cleaned_data['username'], password=newuser_form.cleaned_data['password2'])
            auth.login(request, newuser)
            return redirect('http://127.0.0.1:8000')
        else:
            args['form'] = newuser_form
    return render_to_response('register.html', args)



















