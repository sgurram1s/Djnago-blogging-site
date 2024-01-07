from django.contrib import admin
from django.urls import path
from feed.views import *

app_name = 'feed'

urlpatterns = [
    path('<str:user>/', index, name='index'),
    path('<str:user>/createpost/', createpost, name='createpost'),
    path('<str:user>/viewpost/<int:post_id>/', viewpost, name='viewpost'),
]
