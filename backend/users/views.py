from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def usersIndex(request, users_page):
    if request.GET:
        print(request.GET)

    return HttpResponse(f'<h1>Страница приложения Пользователей</h1><p>{users_page}</p>')