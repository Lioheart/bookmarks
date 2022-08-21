from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from .forms import LoginForm


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
        return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    """
    Strona główna.

    :rtype: object
    """
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})
