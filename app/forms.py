from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Neighbourhood,Post,Profile,Comment,Neighbourhood_infrastructure

class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class NeighbourhoodForm(forms.ModelForm):
    class Meta:
        model = Neighbourhood
        exclude = ['user']   

class UpdateUserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['user']         

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['user', 'post']  

class NeighbourhoodInfrastructureForm(forms.ModelForm):
    class Meta:
        model = Neighbourhood_infrastructure
        exclude = ['user']    
