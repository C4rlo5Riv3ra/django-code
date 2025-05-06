from django.urls import path 
from . import views 

urlpatterns = [ 
    path('perfil/', views.profile_view, name='profile'), 
    path('perfil/actualizar/', views.profile_update, name='profile_update'), 
] 