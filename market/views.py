from django.shortcuts import render, redirect
from django.http import HttpResponse


def initial_page(request):
    if request.user.is_authenticated:
        user = request.user
        return redirect('feed:index', user)
    return render(request, 'market/initial_page.html')