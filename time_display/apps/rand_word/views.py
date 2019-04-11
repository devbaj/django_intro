from django.shortcuts import render, redirect, HttpResponse
from django.utils.crypto import get_random_string

# Create your views here.

def index(request):
    
    if 'counter' in request.session:
        request.session["counter"] += 1
    else:
        request.session["counter"] = 1
    
    context={
        "word": get_random_string(length=14)
    }
    return render(request, "rand_word/index.html", context)

def new(request):
    
    return redirect("/random_word")

def reset(request):
    request.session.clear()
    
    return redirect("/random_word")