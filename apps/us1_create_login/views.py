from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import BloomSignupForm

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
    if request.user.is_authenticated:
        return redirect("calendar")

    if request.method == "POST":
        form = BloomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Create profile automatically
            UserProfile.objects.get_or_create(user=user)

            # New users always go to onboarding first (US3)
            return redirect("onboarding")
    else:
        form = BloomSignupForm()

    return render(request, "pages/auth/signup.html", {"form": form})


@login_required
def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'You\'ve been logged out. See you soon! 🌸')
    return redirect('login')