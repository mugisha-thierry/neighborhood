from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .models import  Profile,Neighbourhood,Neighbourhood_infrastructure,Post
from django.contrib.auth import login, authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import SignUpForm, NeighbourhoodForm, PostForm,UpdateUserProfileForm,CommentForm,NeighbourhoodInfrastructureForm
from .models import  Profile,Neighbourhood,Neighbourhood_infrastructure,Post,Comment
from .decorators import admin_only,allowed_users

# Create your views here.



@login_required(login_url='login')
@admin_only
def home(request):
    neighbourhood_infrastructures = Neighbourhood_infrastructure.objects.all()
    posts = Post.objects.all()
    users = User.objects.exclude(id=request.user.id)
    form = PostForm(request.POST or None, files=request.FILES)      
    if form.is_valid():
        post=form.save(commit=False)
        post.user = request.user.profile
        post.save()
        return redirect('home')
    context = {
        'posts': posts,
        'form': form,
        'users':users,
        'neighbourhood_infrastructures':neighbourhood_infrastructures
    }
    return render(request, 'home.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name = 'normal_users')
            user.groups.add(group)
            return redirect("/")
    else:
        form = SignUpForm()
    return render(request, 'register/register.html', {'form': form})  

@login_required(login_url='login')
@allowed_users(allowed_roles=['system_administrator'])
def system_admin(request):
    users = User.objects.exclude(id=request.user.id)
    neighbourhoods = Neighbourhood.objects.all()

    context = {
        'neighbourhoods': neighbourhoods,
        'users':users,
    }
    return render(request, 'system_admin.html', context)

@allowed_users(allowed_roles=['system_administrator'])
def edit_neighbourhood(request, neighbourhood_name):
    neighbourhood = get_object_or_404(Neighbourhood, neighbourhood_name=neighbourhood_name)
    if request.method == 'POST':
        form = NeighbourhoodForm(request.POST, instance=neighbourhood)
        if form.is_valid():
            form.save()
            return redirect('system_admin')
        else:
            form = NeighbourhoodForm(instance=neighbourhood)
    else:
        form = NeighbourhoodForm(instance=neighbourhood)
    return render(request, 'create_neighbourhood.html', {'form':form, 'neighbourhood':neighbourhood}) 

@allowed_users(allowed_roles=['system_administrator'])
def del_neighbourhood(request, neighbourhood_name):
    neighbourhood = get_object_or_404(Neighbourhood, neighbourhood_name=neighbourhood_name)
    neighbourhood.delete()
    return redirect('system_admin') 

@allowed_users(allowed_roles=['system_administrator'])
def del_user(request, username):
    user = get_object_or_404(User, username=username)
    user.delete()
    return redirect('system_admin')     
      



@login_required(login_url='login')
@allowed_users(allowed_roles=['system_administrator'])
def create_neighbourhood(request):
    form = NeighbourhoodForm(request.POST or None, files=request.FILES)
    if form.is_valid():
        neighbourhood=form.save(commit=False)
        neighbourhood.user = request.user.profile
        neighbourhood.save()
        return redirect('system_admin')
    return render(request, 'create_neighbourhood.html', {'form': form})


def profile(request, username):
    posts = request.user.profile.posts.all()
    if request.method == 'POST':
        prof_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if prof_form.is_valid():
            prof_form.save()
            return redirect(request.path_info)
    else:
        prof_form = UpdateUserProfileForm(instance=request.user.profile)
    if request.method == "POST":
        form = PostForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user.profile
            post.save()
    else:
        form = PostForm()

    context = {
        'prof_form': prof_form,
        'posts': posts,
        'form':form,

    }
    return render(request, 'profile.html', context)    

def post(request,id):
    post = Post.objects.get(id = id)
    comments = Comment.objects.order_by('-date')
    current_user = request.user
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('post', args=(post.id,)))
    else:
        form = CommentForm()
    context={"post":post,"comments":comments,"form":form}
    return render(request, 'post.html',context)   


@login_required(login_url='login')
@allowed_users(allowed_roles=['neighbourhood_admin'])
def neighbourhood_admin(request):
    neighbourhood_infrastructures = Neighbourhood_infrastructure.objects.all()
    posts = Post.objects.all()
    users = User.objects.exclude(id=request.user.id)
    form = PostForm(request.POST or None, files=request.FILES)      
    if form.is_valid():
        post=form.save(commit=False)
        post.user = request.user.profile
        post.save()
        return redirect('home')
    context = {
        'posts': posts,
        'form': form,
        'users':users,
        'neighbourhood_infrastructures':neighbourhood_infrastructures
    }   
    return render(request,'neighbourhood_admin.html',context)


@allowed_users(allowed_roles=['neighbourhood_admin'])
def create_neighbourhood_info(request):
    form = NeighbourhoodInfrastructureForm(request.POST or None, files=request.FILES)
    if form.is_valid():
        infrastructure=form.save(commit=False)
        infrastructure.user = request.user.profile
        infrastructure.save()
        return redirect('neighbourhood_admin')
    return render(request, 'create_neighbourhood_info.html', {'form': form})    

def search_department(request):
    if 'searchproject' in request.GET and request.GET["searchproject"]:
        search_term = request.GET.get("searchproject")
        searched_project = Neighbourhood_infrastructure.search_by_Neighbourhood_infrastructure(search_term)
        message = f"{search_term}"
        context = {'neighbourhood_infrastructures':searched_project,'message': message}

        return render(request, "search.html",context)
    else:
      message = "You haven't searched for any term"
      return render(request, 'search.html',{"message":message})   