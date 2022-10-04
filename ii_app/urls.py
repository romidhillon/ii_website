from . import views
from django.urls import path



urlpatterns = [

    # ii_app/
    path('', views.main, name=''),

    path('resources', views.resources, name='resources'),
    
    path('resources/<int:id>/<int:id_2>/', views.resource_detail, name='resource_detail'),

    path('addrisks/', views.risk_form, name='risk_form'),

    path('update/<int:risk_id>/', views.update_risk_item, name='update_risk_item'),
 
    path('delete/<int:risk_id>/', views.delete_risk_item, name='delete_risk_item'),

    path('riskregister/', views.risk_register, name='riskregister/'),

    path('margin/', views.margin, name='margin'),

    path('finances', views.finances, name='finances'),

    path('finances/<str:code>/', views.finance_detail, name='finance_detail'),
    
    path('cv/', views.cv, name='cv'),
]

