# sources / code from:
# https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
# https://www.ordinarycoders.com/blog/article/django-user-register-login-logout
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect


def signup(request):
    if request.user.is_authenticated:
        return redirect('polls:index')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            return redirect('polls:index')
    else:
        form = UserCreationForm()
    return render(request, 'polls/signup.html', {'form': form})


def login(request):
    if request.user.is_authenticated:
        return redirect('polls:index')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                redirect_url = request.GET.get('next')
                if redirect_url:
                    return redirect(redirect_url)
                return redirect('polls:index')
    else:
        form = AuthenticationForm()
    return render(request, 'polls/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('polls:index')
