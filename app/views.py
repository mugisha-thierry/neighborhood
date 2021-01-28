from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import SignUpForm

# Create your views here.

def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['username']
            email = form.cleaned_data['email']
            form.save()
            return redirect("/")
    else:
        form = SignUpForm()
    return render(request, 'register/register.html', {'form': form})    

def index(request):
    try:
        if not request.user.is_authenticated:
            return redirect('/accounts/login/')
        current_user=request.user
        profile =Profile.objects.get(username=current_user)
    except ObjectDoesNotExist:
        return redirect('create-profile')

    return render(request,'index.html')

@login_required(login_url='/accounts/login/')
def user_profile(request,username):
    user = User.objects.get(username=username)
    profile =Profile.objects.get(username=user)

    return render(request,'user_profile.html',{"profile":profile})

@login_required(login_url='/accounts/login/')
def create_profile(request):
    current_user=request.user
    if request.method=="POST":
        form =ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            profile = form.save(commit = False)
            profile.username = current_user
            profile.save()
        return HttpResponseRedirect('/')

    else:

        form = ProfileForm()
    return render(request,'profile_form.html',{"form":form})  

@login_required(login_url='/accounts/login/')
def update_profile(request):
    current_user=request.user
    if request.method=="POST":
        instance = Profile.objects.get(username=current_user)
        form =ProfileForm(request.POST,request.FILES,instance=instance)
        if form.is_valid():
            profile = form.save(commit = False)
            profile.username = current_user
            profile.save()

        return redirect('index')

    elif Profile.objects.get(username=current_user):
        profile = Profile.objects.get(username=current_user)
        form = ProfileForm(instance=profile)
    else:
        form = ProfileForm()

    return render(request,'update_profile.html',{"form":form})  

@login_required(login_url='/accounts/login/')
def authorities(request):
    current_user=request.user
    profile=Profile.objects.get(username=current_user)
    authorities = Authorities.objects.filter(neighbourhood=profile.neighbourhood)

    return render(request,'authorities.html',{"authorities":authorities})   

@login_required(login_url='/accounts/login/')
def health(request):
    current_user=request.user
    profile=Profile.objects.get(username=current_user)
    health = Health.objects.filter(neighbourhood=profile.neighbourhood)

    return render(request,'health.html',{"health":health})     

@login_required(login_url='/accounts/login/')
def post(request):
    current_user=request.user
    profile=Profile.objects.get(username=current_user)
    posts = Post.objects.filter(neighbourhood=profile.neighbourhood)

    return render(request,'post.html',{"posts":posts})      

@login_required(login_url='/accounts/login/')
def new_post(request):
    current_user=request.user
    profile =Profile.objects.get(username=current_user)

    if request.method=="POST":
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit = False)
            post.username = current_user
            post.neighbourhood = profile.neighbourhood
            post.avatar = profile.avatar
            post.save()

        return HttpResponseRedirect('/post')

    else:
        form = PostForm()

    return render(request,'post_form.html',{"form":form})    
    

@login_required(login_url='/accounts/login/')
def search_results(request):
    if 'post' in request.GET and request.GET["post"]:
        search_term = request.GET.get("post")
        searched_posts = Post.search_post(search_term)
        message=f"{search_term}"

        print(searched_posts)

        return render(request,'search.html',{"message":message,"posts":searched_posts})

    else:
        message="You haven't searched for any term"
        return render(request,'search.html',{"message":message})  