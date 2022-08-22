from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile


def user_login(request):
    """
    Logowanie użytkownika.

    Metoda is_valid sprawdza poprawność wypełnienia formularzy.
    Metoda cleaned_data zapisuje formularze w formie słownika.
    Funkcja authenticate służy do sprawdzania, czy użytkownik istnieje w bazie i zwraca obiekt User lub None.
    Funkcja login tworzy sesję użytkownika.
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])  # metoda sprawdza, czu user jest w bazie
            if user is None:
                return HttpResponse('Nieprawidłowe dane uwierzytelniające.')
            if user.is_active:
                login(request, user)  # tworzy sesje użytkownika-właściwe zalogowanie
                return HttpResponse('Uwierzytelnienie zakończyło się sukcesem.')
            else:
                return HttpResponse('Konto jest zablokowane.')
    else:
        form = LoginForm()
        return render(request, 'account/templates/registration/login.html', {'form': form})


@login_required
def dashboard(request):
    """
    Strona główna.

    :rtype: object
    """
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def register(request):
    """
    Witryna rejestracji nowego użytkownika.
    :rtype: object
    """
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Utworzenie nowego obiektu użytkownika; jeszcze nie zapisujemy w bazie
            new_user = user_form.save(commit=False)

            # Ustawienie wybranego hasła
            new_user.set_password(user_form.cleaned_data['password'])

            # Zapisanie obiektu User
            new_user.save()

            # Utworzenie profilu użytkownika
            profile = Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Uaktualnienie profilu zakończyło się sukcesem.')
        else:
            messages.error(request,'Wystąpił błąd podczas uaktualniania profilu.')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})
