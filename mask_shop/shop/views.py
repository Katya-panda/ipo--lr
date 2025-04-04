from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def home(request):
    return render(request, 'shop/home.html')  # Обратите внимание на путь

def about(request):
    return render(request, 'shop/about.html')

def author(request):
    return render(request, 'shop/author.html')