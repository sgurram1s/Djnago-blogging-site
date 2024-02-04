from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class FeedPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200) # CharField is for limited text
    post_content = models.TextField() # TextField is for unlimited text
    created_date = models.DateTimeField(default=timezone.now)
    locations = models.ManyToManyField('PostLocation',blank=True)

    def __str__(self):
        return self.title
    
    def postid(self):
        return self.id

    def body_snippet(self):
        if len(self.post_content) > 150:
            return self.post_content[:150] + '.........'
        else:
            return self.post_content

class PostLocation(models.Model):
    post_location = models.CharField(max_length=200)

    def __str__(self):
        return self.post_location


class PostLikeData(models.Model):
    post = models.OneToOneField(FeedPost, on_delete=models.CASCADE, primary_key=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    def __str__(self):
        return self.post.title
    
    def like_count(self):
        return self.likes.count()