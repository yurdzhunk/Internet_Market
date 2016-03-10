from django.shortcuts import render

from django.shortcuts import render_to_response, redirect

def start_page(request):
    return render_to_response('start_page.html')
