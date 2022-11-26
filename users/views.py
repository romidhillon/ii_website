from django.shortcuts import redirect, render
from django.contrib import messages
from users.forms import SignInForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile, Post
from .forms import EditProfileForm, EditUserForm, PostCreateForm


# Create your views here.

def sign_up (request):
    sign_up_form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            print(new_user)
            username = form.cleaned_data.get('username')
            Profile.objects.create(user = new_user)
            messages.success(request,f'Hi {username}, you have successfully created your account. Please sign-in to continue.')
            return redirect('../sign_in/')
        
            # Profile.objects.create(user = request.user)
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
        user_profile = EditProfileForm(instance=request.user.profile, data = request.POST, files = request.FILES)
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
def post_creation (request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
    else: 
        form = PostCreateForm()

    context = {
        'form': form
    }
    return render(request,'users/post_creation.html',context)

@login_required
def posts (request):
    posts = Post.objects.all()
    context = {
        'posts':posts
    }

    return render (request,'users/posts.html',context)

def sign_out(request):
    logout(request)
    return redirect('sign_in')


@login_required
def profile_page (request):
    return render(request,'users/profile.html')






          # username = request.POST.get('username')
        # password = request.POST.get('password1')

        # user = authenticate(request = username, password = password)

        # if user is not None: 
        #     login(request, user)
        #     return redirect('')