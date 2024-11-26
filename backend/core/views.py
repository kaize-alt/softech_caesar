from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from items.models import *

# Create your views here.
menu = ['О сайте', 'Обратная связь', 'Контакты']

def home(request):
    posts = Product.objects.all()
    return render(request, 'core/home.html', {'posts': posts, 'title': 'Главная страница', 'menu': menu})

def about(request):
    return render(request, 'core/about.html', {'title': 'О нас', 'menu': menu})

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>', status = 404)