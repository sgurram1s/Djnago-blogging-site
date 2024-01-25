from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import FeedPost, PostLikeComment
from .forms import CreatePostForm
from users_register.models import MyProfile


@login_required(login_url='users_register:login_page')
def index(request, **kwargs):
    user_name = kwargs['user']
    feed_posts = FeedPost.objects.all().order_by('-created_date')
    profile_data = MyProfile.objects.all()
    context = {
        'feed_posts': feed_posts,
        'user_id': user_name,
        'profile_data': profile_data,
    }

    return render(request, 'feed/postfeed.html', context)

@login_required(login_url='users_register:login_page')
def createpost(request, user):
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            form = FeedPost.objects.create(
                author=request.user,
                title= form.cleaned_data['title'],
                post_content= form.cleaned_data['post_content'],
            )

            form.save()
            location = request.POST.getlist('locations')
            form.locations.set(location)
            return redirect('feed:index', user=user)
    if request.method == 'GET':
        form = CreatePostForm()


    return render(request, 'feed/createpost.html',{'form': form} )


def viewpost(request, user, post_id):
    post = FeedPost.objects.get(id=post_id)
    profile_data = MyProfile.objects.get(user=post.author)
    context = {
        'data': post,
        'user_id': user,
        'profile_data': profile_data,
    }
    return render(request, 'feed/viewpost.html', context)

def postcomment(request, post_id):
    post = PostLikeComment.objects.get(id=post_id)

    context = {
        'data': post,
        #'user': user,
    }
    return context
    