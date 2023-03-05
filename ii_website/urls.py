from django.contrib import admin
from django.urls import include,path
from django.conf import settings 
from django.conf.urls.static import static
from users import views as user_views
from django.contrib.auth import views as authentication_views
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',lambda r: redirect('ii_app/') ),
    path('ii_app/', include('ii_app.urls')),
    path('sign_up/',user_views.sign_up, name= 'sign_up'),
    path('sign_in/',user_views.sign_in, name= 'sign_in'),
    path('sign_out/',user_views.sign_out, name= 'sign_out'),

    path('reset_password/',authentication_views.PasswordResetView.as_view(template_name = "users/password_reset.html"), name= 'reset_password'),

    path('reset_password_sent/',authentication_views.PasswordResetDoneView.as_view(template_name = "users/password_reset_sent.html"), name= 'password_reset_done'),

    path('reset/<uidb64>/<token>/',authentication_views.PasswordResetConfirmView.as_view(template_name = "users/password_reset_form.html"), name= 'password_reset_confirm'),
    
    path('reset_password_complete/',authentication_views.PasswordResetCompleteView.as_view(template_name = "users/password_reset_done.html"), name= 'password_reset_complete'),

    path('profile/',user_views.profile_page,  name= 'profile'),
    
    path('edit/',user_views.edit,  name= 'edit'),

    path('posts/',user_views.posts,  name= 'posts'),

    path('like_post/<int:pk>/',user_views.likes,  name= 'like_post'),

    path('comment_post/<int:pk>/',user_views.comments,  name= 'comment_post'),


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


