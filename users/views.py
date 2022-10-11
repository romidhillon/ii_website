from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def sign_up (request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Hi {username}, you have successfully signed up to the Intelligent Infrastructure application')
            return redirect('../login/')
    else:
        form = UserCreationForm()

    context = {
        'form':form,
    }
    return render(request,'users/sign_up.html',context)


@login_required
def profile_page (request):
    return render(request,'users/profile.html')