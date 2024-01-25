from typing import Any
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, related_name='friends', blank=True)
    
    objects = [User]
    
    def __str__(self):
        return self.user.username

class MyProfile(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    birthday = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_photo = models.ImageField(blank=True, null=True, default='default.jpg', upload_to='profile_pics')
    created = models.DateTimeField(default=timezone.now)

    
    def __str__(self):
        return self.user.username

    