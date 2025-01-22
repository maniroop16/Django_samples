from django.shortcuts import render
from testingapp.templates import *
from .models import *
# Create your views here.

def main(request):
    context = {}
    return render(request, 'base.html', context)

def store(request):
    all_products = Product.objects.all()
    context = {"products": all_products}
    return render(request, 'store.html', context)

def cart(request):
    context = {}
    return render(request, 'cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'checkout.html', context)
