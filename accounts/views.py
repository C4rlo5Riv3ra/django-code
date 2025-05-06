from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages 
from django.contrib.auth.forms import AuthenticationForm 
from .models import Usuario, Perfil

@login_required 
def profile_view(request): 
    """Vista para mostrar el perfil del usuario""" 
    context = { 
        'user': request.user, 
    } 
    return render(request, 'accounts/profile.html', context) 

@login_required 
def profile_update(request): 
    """Vista para actualizar el perfil del usuario""" 
    if request.method == 'POST': 
        user = request.user 
        # Actualizar datos del usuario 
        user.full_name = request.POST.get('full_name') 
        user.email = request.POST.get('email') 
        user.mobile = request.POST.get('mobile') 
        user.save() 
        messages.success(request, 'Perfil actualizado correctamente.') 
        return redirect('profile') 
    return redirect('profile') 

def login_view(request): 
    """Vista para el login de usuarios""" 
    if request.user.is_authenticated: 
        return redirect('home') 
    if request.method == 'POST': 
        form = AuthenticationForm(request, data=request.POST) 
        if form.is_valid(): 
            username = form.cleaned_data.get('username') 
            password = form.cleaned_data.get('password') 
            user = authenticate(username=username, password=password)
            if user is not None: 
                login(request, user) 
                messages.success(request, f'Bienvenido, {user.full_name}!') 
                # Redirigir a la página solicitada o a home 
                next_page = request.GET.get('next') 
                if next_page: 
                    return redirect(next_page) 
                return redirect('home') 
            else: 
                messages.error(request, 'Usuario o contraseña incorrectos.') 
        else: 
            messages.error(request, 'Usuario o contraseña incorrectos.') 
    else: 
        form = AuthenticationForm() 
    context = { 
        'form': form, 
    } 
    return render(request, 'accounts/login.html', context)

def logout_view(request): 
    """Vista para cerrar sesión""" 
    logout(request) 
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('login')