from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, request
from .forms import RegisterForm, MyProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UserData, MyProfile
from django.contrib import messages
from .decoders import unauthenticated_user, allowed_users

@unauthenticated_user
def register_page(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if User.objects.filter(username=username).exists():
                messages.error(request, f'User already exists! Please login')
        elif User.objects.filter(email=email).exists():
            messages.error(request, f'Email already exists! Please use another email')
        elif form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username = username, password = password)
            userdata = UserData.objects.create(user=user)
            userdata.save()
            login(request, user)
            messages.success(request, f'Account created for {username}!')
            messages.success(request, f'Please add your personal details')
            return redirect('users_register:personal_info_page', request.user)
        else:
            if password1 != password2:
                messages.error(request, f'Passwords do not match! Please try again')
            else:
                messages.error(request, f'Password must be at least 8 characters long')
                messages.error(request, f'Password must contains Capital letters, Small letters, Numbers and Special characters')
        return render(request, 'users_register/register_page.html', {'form': form})
    else:
        form = RegisterForm()
    return render(request, 'users_register/register_page.html', {'form': form})


@login_required(login_url='users_register:login_page')
def personal_info_page(request, user):
    if request.method == 'POST':        
        form = MyProfileForm(request.POST,request.FILES)
        if form.is_valid():
            user_object = MyProfile.objects.create(
                first_name = form.cleaned_data.get('first_name'),
                last_name = form.cleaned_data.get('last_name'),
                user = request.user,
                birthday = form.cleaned_data.get('birthday'),
                phone = form.cleaned_data.get('phone'),
                profile_photo = form.files.get('profile_photo'),
                )
            user_object.save()

            return redirect('feed:index', user)
        else:
            messages.error(request, f'Please enter valid details')
            return render(request, 'users_register/personal_info_page.html', {'form': form})
    else:            
        form = MyProfileForm(initial={'user': request.user})
    return render(request, 'users_register/personal_info_page.html', {'form': form})

#need to modify this function and add this to the personal_info_page function
@login_required(login_url='users_register:login_page')
def personal_info_update(request, user):
    if request.method == 'POST':        
        form = MyProfileForm(request.POST,request.FILES)
        if form.is_valid():
            MyProfile.objects.filter(user=request.user).update(
                first_name = form.cleaned_data.get('first_name'),
                last_name = form.cleaned_data.get('last_name'),
                user = request.user,
                birthday = form.cleaned_data.get('birthday'),
                phone = form.cleaned_data.get('phone'),
                )
            data = request.user
            return redirect('users_register:profile_page', user, data)
        else:
            messages.error(request, f'Please enter valid details')
            return render(request, 'users_register/personal_info_update.html', {'form': form})
    else:            
        form = MyProfileForm(instance=request.user.myprofile)
    return render(request, 'users_register/personal_info_update.html', {'form': form})


@unauthenticated_user
def login_page(request):   
    if request.method == 'POST':
        form = AuthenticationForm(data= request.POST)
        if form.is_valid():
            user = form.get_user()
            #user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request, user) 
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect('feed:index', user)
            else:
                messages.info(request, f'Invalid username or password')
        else:
            username = form.cleaned_data.get('username')
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Invalid password! Please try again')
            else:
                messages.info(request, f'User does not exist! Please register')
        return render(request, 'users_register/login_page.html', {'form': form})
    else:
        form = AuthenticationForm()
    return render(request, 'users_register/login_page.html', {'form': form})


def logout_page(request):
    logout(request)
    return redirect("initial_page")


@login_required(login_url='users_register:login_page')
def friends_page(request, user):
    if request.method == 'POST':
        if request.POST.get("unfriend"):
            user=request.user.id
            friend = request.POST.get("unfriend")
            UserData.objects.get(user=user).friends.remove(friend)
    user = request.user.id
    friends = UserData.objects.get(user=user).friends.all().order_by('username')
    profile_data = MyProfile.objects.all()
    context = {
        'friends': friends,
        'number_of_friends': len(friends),
        'profile_data': profile_data,
        }
    return render(request, "users_register/friends_page.html", context)

@login_required(login_url='users_register:login_page')
def profile_page(request, user, **kwargs):
    user_profile = kwargs['data']
    users = User.objects.get(username=user_profile)
    details = MyProfile.objects.get(user=users)
    list_of_friends = UserData.objects.get(user=request.user).friends.all()
    
    if request.method == 'POST':
        if request.POST.get("editprofile"):
            return redirect('users_register:personal_info_update', request.user)
        elif request.POST.get("addfriend"):
            friend = request.POST.get("addfriend")
            UserData.objects.get(user=request.user).friends.add(friend)
        elif request.POST.get("removefriend"):
            friend = request.POST.get("removefriend")
            UserData.objects.get(user=request.user).friends.remove(friend)
        return redirect('feed:index', user)
            
    
    if users.username != user and (users not in list_of_friends):
        follow = "Add Friend"
    elif users.username != user:
        follow = "Remove Friend"
    else:
        follow = "Edit Profile"
    context = {
        'user': users,
        'details': details,
        'follow': follow,
        }
    return render(request, "users_register/profile_page.html", context)

