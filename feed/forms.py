from django import forms
from .models import FeedPost, PostLocation

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = FeedPost
        fields = ['title', 'post_content', 'locations']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Content'}),
            'locations': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }