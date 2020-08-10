from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import User


class UserAdmin(admin.ModelAdmin):
    """
    Класс для работы с моделью пользователя в админке
    """
    list_display = ('id', 'first_name', 'last_name', 'date_of_birth', 'score')
    list_display_links = ('id', 'first_name', 'last_name')
    # list_editable = ('first_name', 'last_name')
    fields = ('first_name', 'last_name', 'date_of_birth', 'get_age', 'photo', 'score', 'get_photo')
    readonly_fields = ('get_age', 'get_photo')

    def get_photo(self, obj):
        """
        метод для отображения фотографии пользователя в админке
        """
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="200">')
        return '---'
    get_photo.short_description = 'Миниатюра'


admin.site.register(User, UserAdmin)
