from . import views
from django.urls import path


urlpatterns = [

    # ii_app/
    path('', views.main, name=''),

    path('resources', views.resources, name='resources'),
]
