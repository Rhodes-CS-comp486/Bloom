from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

def login_view(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back! 🌸')
                next_page = request.GET.get('next', 'dashboard')
                return redirect(next_page)
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = AuthenticationForm()

    return render(request, 'pages/auth/login.html', {'form': form})

def signup_view(request):
    """Handle user registration"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome to Bloom! 🌸')
            return redirect('onboarding')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = UserCreationForm()

    return render(request, 'pages/auth/signup.html', {'form': form})

@login_required
def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'You\'ve been logged out. See you soon! 🌸')
    return redirect('login')