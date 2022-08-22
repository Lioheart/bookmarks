from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Użytkownik')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Data urodzin')
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True, verbose_name='Zdjęcie')

    def __str__(self):
        return f'Profil użytkownika {self.user.username}'

    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profile'