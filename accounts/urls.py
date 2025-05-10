from django.urls import path 
from accounts.views import login_view, logout_view
from . import views 

urlpatterns = [ 
    path('perfil/', views.profile_view, name='profile'), 
    path('perfil/actualizar/', views.profile_update, name='profile_update'), 
    
    # URLs de autenticación
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
] 