"""ii_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# the library below has been added so that the ii_app urls path could be included in this file. 
from django.urls import include,path
from django.conf import settings 
from django.conf.urls.static import static
from users import views as user_views
from django.contrib.auth import views as authentication_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ii_app/', include('ii_app.urls')),
    path('sign_up/',user_views.sign_up, name= 'sign_up'),
    path('sign_in/',user_views.sign_in, name= 'sign_in'),
    path('sign_out/',user_views.sign_out, name= 'sign_out'),

    path('reset_password/',authentication_views.PasswordResetView.as_view(template_name = "users/password_reset.html"), name= 'reset_password'),

    path('reset_password_sent/',authentication_views.PasswordResetDoneView.as_view(template_name = "users/password_reset_sent.html"), name= 'password_reset_done'),

    path('reset/<uidb64>/<token>/',authentication_views.PasswordResetConfirmView.as_view(template_name = "users/password_reset_form.html"), name= 'password_reset_confirm'),
    
    path('reset_password_complete/',authentication_views.PasswordResetCompleteView.as_view(template_name = "users/password_reset_done.html"), name= 'password_reset_complete'),


    path('profile/',user_views.profile_page,  name= 'profile'),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


