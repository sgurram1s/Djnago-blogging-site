from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from .forms import RegisterForm, MyProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UserData, MyProfile



def register_page(request):
    if request.user.is_authenticated:
        user = request.user
        return redirect('feed:index', user)
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username = username, password = password)
            login(request, user)
            return redirect('users_register:personal_info_page', request.user)
        else:
            return render(request, 'users_register/register_page.html', {'form': form})
    else:
        form = RegisterForm()
    return render(request, 'users_register/register_page.html', {'form': form})


@login_required(login_url='users_register:login_page')
def personal_info_page(request, user):
    if request.method == 'POST':
        form = MyProfileForm(request.POST)
        if form.is_valid():
            user_data = MyProfile.objects.create(
                first_name = form.cleaned_data.get('first_name'),
                last_name = form.cleaned_data.get('last_name'),
                user = request.user,
                birthday = form.cleaned_data.get('birthday'),
                phone = form.cleaned_data.get('phone'),
                )
            user_data.save()
            return redirect('feed:index', user)
        else:
            return HttpResponse('details not valid')
    else:
        form = MyProfileForm()
    return render(request, 'users_register/personal_info_page.html', {'form': form})

def login_page(request):   
    if request.user.is_authenticated:
        user = request.user
        return redirect('feed:index', user)
    if request.method == 'POST':
        form = AuthenticationForm(data= request.POST)
        if form.is_valid():
            user = form.get_user()
            #user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request, user)                
                return redirect('feed:index', user)
            else:
                return HttpResponse('Invalid Credentials')
        else:
            return render(request, 'users_register/login_page.html', {'form': form})
    else:
        form = AuthenticationForm()
    return render(request, 'users_register/login_page.html', {'form': form})


def logout_page(request):
    logout(request)
    return redirect("initial_page")


@login_required(login_url='users_register:login_page')
def friends_page(request, user):
    user = request.user.id
    friends = UserData.objects.get(user=user).friends.all().order_by('username')
    context = {
        'friends': friends,
        'number_of_friends': len(friends)
        }
    return render(request, "users_register/friends_page.html", context)

@login_required(login_url='users_register:login_page')
def profile_page(request, user):
    user = User.objects.get(username=user)
    details = MyProfile.objects.get(user=user)
    context = {
        'user': user,
        'details': details,
        }
    return render(request, "users_register/profile_page.html", context)
