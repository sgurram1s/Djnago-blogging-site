from django.contrib import admin
from .models import FeedPost, PostLocation, PostLikeComment

admin.site.register(FeedPost)
admin.site.register(PostLocation)
admin.site.register(PostLikeComment)