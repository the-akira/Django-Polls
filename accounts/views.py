from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages

def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created. You can log in now!')   
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:               
                login(request, user)
                messages.success(request, f'Login successful!')
                return redirect('index')
    else:
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'accounts/login.html', context)

@login_required
def logout_view(request):
    messages.success(request, 'Logout successful!')
    logout(request)
    return redirect('index')

@login_required 
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('accounts:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'total_votes': len(request.user.vote_set.all())
    }
    return render(request, 'accounts/profile.html', context)