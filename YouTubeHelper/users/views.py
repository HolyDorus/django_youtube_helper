from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import logout, authenticate, login

from .forms import LoginForm, RegisterForm


class LogoutView(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('main:index')


class LoginView(View):
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:index')

        context = {
            'form': LoginForm()
        }

        return render(request, 'users/login.html', context)

    def post(self, request, *args, **kwargs):
        context = self.authorize_or_get_error(request)

        if request.user.is_authenticated:
            return redirect('main:index')
        else:
            return render(request, 'users/login.html', context)

    def authorize_or_get_error(self, request):
        data = {}

        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            user = authenticate(
                username=cd['username'],
                password=cd['password']
            )

            if user is not None:
                login(request, user)
                return data
            else:
                data['error'] = 'Введен неправильный логин или пароль!'
        else:
            data['error'] = 'Ошибка валидации данных!'

        data['form'] = form
        return data


class RegisterView(View):
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:index')

        return render(request, 'users/register.html', {'form': RegisterForm()})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main:index')

        return render(request, 'users/register.html', {'form': form})
