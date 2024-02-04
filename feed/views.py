from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import FeedPost, PostLikeData
from .forms import CreatePostForm
from users_register.models import MyProfile
from django.core.mail import send_mail


@login_required(login_url='users_register:login_page')
def index(request, **kwargs):
    if request.method == 'POST':
        if request.POST.get('like'):
            post_id = request.POST.get('like')
            post = PostLikeData.objects.get(post=post_id)
            post.likes.add(request.user)
        elif request.POST.get('unlike'):
            post_id = request.POST.get('unlike')
            post = PostLikeData.objects.get(post=post_id)
            post.likes.remove(request.user)  
        return redirect('feed:index', user=request.user)
    user_name = kwargs['user']
    feed_posts = FeedPost.objects.all().order_by('-created_date')
    profile_data = MyProfile.objects.all()
    likes_data = PostLikeData.objects.all()
    
    context = {
        'feed_posts': feed_posts,
        'user_id': user_name,
        'profile_data': profile_data,
        'likes_data': likes_data,
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
            PostLikeData.objects.create(post=form).save()
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


def delete_post(request, user, post_id):
    post = FeedPost.objects.get(id=post_id)
    post.delete()
    return redirect('feed:index', user=user)

def sending_mails(request):
    if request.method == "POST":
        subject = request.POST['subject']
        message = request.POST['message']
        email_from = request.POST['email']
        recipient_list = request.POST['recipient_list']
        send_mail(subject, message, email_from, recipient_list)
        return redirect('feed:sending_mails')  
    return render(request, 'feed/sending_mails.html')
    