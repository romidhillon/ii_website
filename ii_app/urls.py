from . import views
from django.urls import path

urlpatterns = [

    path('', views.main, name=''),

    path('resources/', views.resources, name='resources'),

    path('resources/<str:name>/', views.resource_detail, name='resource_detail'),

    path('addrisks/', views.risk_form, name='risk_form'),

    path('update/<int:risk_id>/', views.update_risk_item, name='update_risk_item'),
 
    path('delete/<int:risk_id>/', views.delete_risk_item, name='delete_risk_item'),

    path('riskregister/', views.risk_register, name='riskregister/'),

    path('margin/', views.margin, name='margin'),

    path('finances/', views.finances, name='finances'),

    path('finances/<str:code>/', views.finance_detail, name='finance_detail'),
    
    path('cv/', views.cv, name='cv'),
    
    # path('api/', views.api, name='api'),

    path('search/', views.search_bar, name='search'),

    path('bookings/', views.bookings, name='bookings'),

    path('bookings/<str:assignment_code>/', views.booking_form, name='booking_form'),

    path('projects/', views.project_list_api, name = 'projects'),

    path('projects/<int:id>', views.project_list_api_detail, name = 'project_detail')

]

