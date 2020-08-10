from datetime import date
from django.db import models
from django.urls import reverse


class User(models.Model):
    """модель пользователя"""
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    date_of_birth = models.DateField(verbose_name='Дата рождения')
    photo = models.ImageField(upload_to='photos/', verbose_name='Фотография')
    score = models.PositiveSmallIntegerField(default=0, verbose_name='Счет')

    class Meta:
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'
        ordering = ['id',]

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'pk': self.pk})

    def get_age(self):
        """расчет возраста по дате рождения"""
        today = date.today()
        born = self.date_of_birth
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    get_age.short_description = 'Возраст'
