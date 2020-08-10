from django import forms
from .models import User


class UserCreateForm(forms.ModelForm):
    """
    форма для создания нового пользователя
    """
    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'date_of_birth', 'photo'


class UserFilterForm(forms.Form):
    """
    форма для фильтрации в списке пользователей
    """
    last_name = forms.CharField(label='Фамилия', required=False)
    first_name = forms.CharField(label='Имя', required=False)
    sort = forms.ChoiceField(label='Сортировка', required=False, choices=(
        ('pk', 'По id по возрастанию'),
        ('-pk', 'По id по убыванию'),
        ('last_name', 'Фамилия по возрастанию'),
        ('-last_name', 'Фамилия по убыванию'),
        ('first_name', 'Имя по возрастанию'),
        ('-first_name', 'Имя по убыванию'),
        ('date_of_birth', 'Дата рождения по возрастанию'),
        ('-date_of_birth', 'Дата рождения по убыванию'),
    ))
