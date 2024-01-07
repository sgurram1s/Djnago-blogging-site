from django.contrib import admin
from django.urls import path
from users_register.views import *
from django.urls import reverse

app_name = 'users_register'

urlpatterns = [
    path('register/', register_page, name='register_page'),
    path('<str:user>/personal_details/', personal_info_page, name='personal_info_page'),
    path('login/', login_page, name='login_page'),
    path('logout/', logout_page, name='logout_page'),
    #path('<str:user>/', index_page, name='index_page'),
    path('<str:user>/friends/', friends_page, name='friends_page'),
]

