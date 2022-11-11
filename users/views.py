from django.shortcuts import redirect, render
from django.contrib import messages
from users.forms import SignInForm, SignUpForm
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required


# Create your views here.

def sign_up (request):
    sign_up_form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Hi {username}, you have successfully created your account. Please sign-in to continue.')
            return redirect('../sign_in/')
    else:
        form = SignUpForm()

    context = {
        'sign_up_form':sign_up_form,
    }
    return render(request,'users/sign_up.html',context)

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