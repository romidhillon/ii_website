from . import views
from django.urls import path


urlpatterns = [

    # ii_app/
    path('', views.main, name=''),

    path('resources', views.resources, name='resources'),
    
    path('resources/<int:employee_id>/', views.resource_detail, name='resource_detail'),

    path('addrisks/', views.risk_form, name='risk_form'),

]
