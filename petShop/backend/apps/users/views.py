from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.contrib import messages
from .forms import CustomAuthForm, CustomUserCreationForm
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
# Create your views here.

def translate_password_errors(request, form):
    for error in form.errors.values():
        if 'short' in error.__str__():
            messages.error(request, "Пароль должен содержать минимум 8 символов")
        if 'common' in error.__str__():
            messages.error(request, "Пароль слишком простой")
        if 'entirely numeric' in error.__str__():
            messages.error(request, "Пароль должен содержать минимум одну букву")
        if 'match' in error.__str__():
            messages.error(request, "Пароли не совпадают")

def auth(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('core:main')
    form = CustomAuthForm()
    if request.method == 'POST':
        form = CustomAuthForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password) # doesnt the form.is_valid() check it already?

            if user is not None:
                login(request, user)
                messages.success(request, 'Вы успешно авторизовались!')
                return redirect('core:main')
        else:
            # messages.error(request, form.errors)
            messages.error(request, 'Неправильный логин или пароль')

    context = {'form': form}
    return render(request, 'auth.html', context)

@login_required(login_url='users:auth')
def logout_page(request):
    logout(request)
    messages.info(request, 'Вы вышли из аккаунта')
    return redirect('users:auth')

def register(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('core:main')
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('users:auth')
        else:
            messages.error(request, form.errors)
    context = {'form': form}
    return render(request, 'register.html', context)

def account(request):
    User = get_user_model()

    class ExtraForm(forms.ModelForm):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].initial = getattr(request.user, field)
        class Meta:
            model = User
            fields = request.user.get_extra_fields().keys()

    password_form = SetPasswordForm(request.user)
    extra_form = ExtraForm(instance=request.user) if request.user.get_extra_fields() else None

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'avatar':
            request.user.avatar = request.FILES.get('avatar')
            request.user.save()
            messages.success(request, 'Аватар обновлён')

        elif action == 'username':
            request.user.username = request.POST.get('username', request.user.username)
            request.user.save()
            messages.success(request, 'Имя пользователя обновлено')

        elif action == 'email':
            request.user.email = request.POST.get('email', request.user.email)
            try:
                validate_email(request.user.email)
                request.user.save()
                messages.success(request, 'Email обновлён')
            except ValidationError:
                messages.error(request, 'Неправильный email')
            

        elif action == 'details':
            # password_form = SetPasswordForm(request.user, request.POST)
            extra_form = ExtraForm(request.POST, instance=request.user) if request.user.get_extra_fields() else None
            
            valid = True
            # if request.POST.get('new_password1'):
            #     if password_form.is_valid():
            #         password_form.save()
            #         update_session_auth_hash(request, request.user)
            #     else:
            #         valid = False
            if extra_form and not extra_form.is_valid():
                valid = False
            elif extra_form:
                extra_form.save()

            if valid:
                messages.success(request, 'Данные сохранены')
            else:
                translate_password_errors(request, password_form)
                messages.error(request, extra_form.errors)

        return redirect('users:account')

    return render(request, 'account.html', {
        # 'password_form': password_form,
        'extra_form': extra_form,
    })