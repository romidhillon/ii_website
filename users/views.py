from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from users.forms import SignInForm, SignUpForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, Comment
from .forms import EditProfileForm, EditUserForm, PostCreateForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator


def sign_up (request):
    sign_up_form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            print(new_user)
            username = form.cleaned_data.get('username')
            Profile.objects.create(user = new_user)
            messages.success(request,
            f'Hi {username}, you have successfully created your account. Please sign-in to continue.')
            return redirect('../sign_in/')
        
    else:
        form = SignUpForm()

    context = {
        'sign_up_form':sign_up_form,
    }
    return render(request,'users/sign_up.html',context)

@login_required
def edit (request):
    if request.method == 'POST':
        user_form = EditUserForm(instance=request.user, data = request.POST)
        user_profile = EditProfileForm(instance=request.user.profile, 
        data = request.POST, files = request.FILES)
        if user_form.is_valid() and user_profile.is_valid():
            user_form.save()
            user_profile.save()
    else:
        user_form = EditUserForm(instance=request.user)
        user_profile = EditProfileForm(instance=request.user.profile)
    return render (request,'users/edit.html', {'user_form':user_form, 'profile_form':user_profile})


def sign_in (request):
    sign_in_form = SignInForm()
    if request.method == 'POST':
        sign_in_form = SignInForm(request, data = request.POST)
        if sign_in_form.is_valid():
            user = sign_in_form.get_user()
            login(request,user)
            return redirect('')
  
        else:
            messages.info(request, 'Username or Password is incorrect')
       
    context = {
        'sign_in_form':sign_in_form,
    }
    return render(request,'users/sign_in.html',context)

@login_required
def posts (request):
    posts = Post.objects.all()
    pages = Paginator(posts,3)

    num = 1
    if request.GET.get("page"):
        try: 
            num = int(request.GET.get("page"))
            if num > pages.num_pages:
                raise ValueError
        except:
            num = 1
    page = num

    form = PostCreateForm(request.POST)
    if form.is_valid():
        new_item = form.save(commit=False)
        new_item.user = request.user
        new_item.save()
    else: 
        form = PostCreateForm()

    user_posts = request.user.posts.all()

    page_prev_link = None
    page_next_link = None
    if page > 1:
        page_prev_link = f"{reverse('posts')}?page={page - 1}"
    if page < pages.num_pages:
        page_next_link = f"{reverse('posts')}?page={page + 1}"
    
    context = { 
        'form':form,
        'posts':pages.page(page),
        'user_posts': user_posts,
        'page_prev_link': page_prev_link,
        'page_next_link': page_next_link
    }

    return render(request,'users/posts.html',context)


def likes (request, pk):
    post = get_object_or_404(Post, id = pk)

    if post.likes.contains(request.user):
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    
    return HttpResponseRedirect(reverse('posts'))

def comments (request,pk):
    post = get_object_or_404(Post, id = pk)
    comment = Comment(content=request.POST.get("comment"),user=request.user)
    post.comment_set.add(comment, bulk=False)

    return HttpResponseRedirect(reverse('posts'))
    
def sign_out(request):
    logout(request)
    return redirect('sign_in')


@login_required
def profile_page (request):
    
    
    first_name = User.objects.get(username=request.user).first_name
    last_name = User.objects.get(username=request.user).last_name
    username = User.objects.get(username=request.user).username
    last_login = User.objects.get(username=request.user).last_login
    email = User.objects.get(username=request.user).email
    date_joined = User.objects.get(username=request.user).date_joined

    
    context = {
        'first_name': first_name,
        'last_name': last_name,
        'username': username,
        'email':email,
        'last_login':last_login,
        'date_joined': date_joined,
    }

    return render(request,'users/profile.html',context)





    # paginator = Paginator(user_posts,3)
    # page = request.GET.get('page')

    # try:
    #     posts = paginator.page(page)
    # except PageNotAnInteger:
    #     posts = paginator.page(1)
    # except EmptyPage:
    #     posts = paginator.page(paginator.num_pages)

    # context = { 
    #     'form': form,
    #     'posts':posts,
    #     'user_posts': user_posts,
    #     'page':page,
    # }

    # return render(request,'users/posts.html',context)

    # from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger

    # from django.contrib.auth import authenticate, 

    # from typing_extensions import Self