from django.db import transaction
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView
from django.views.generic.edit import DeleteView
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.response import Response

from .forms import UserCreateForm, UserFilterForm
from .models import User
from .serializers import UserScoreSerializer
from .utils import export_to_excel

MAX_SCORE = 10


class ScoresListView(ListAPIView):
    """
    вывод счета в голосовании всех пользователей
    """
    queryset = User.objects.all()
    serializer_class = UserScoreSerializer


class ScoreDetailView(RetrieveUpdateAPIView):
    """
    вывод и обновление счета в голосовании конкретного пользования
    """
    queryset = User.objects.all()
    serializer_class = UserScoreSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.score < MAX_SCORE:
            with transaction.atomic():
                user = User.objects.select_for_update().filter(pk=instance.id, score__lt=MAX_SCORE).get()
                user.score += 1
                user.save()
            instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


def poll_view(request):
    """
    вывод страницы голосования
    """
    users = User.objects.all()
    return render(request, 'main/poll.html', {'users': users})


def list_users(request):
    """
    вывод списка пользователей с возможностью фильтрации
    """
    users = User.objects.all()
    form = UserFilterForm(request.GET)
    if form.is_valid():
        if form.cleaned_data['last_name']:
            users = users.filter(last_name__icontains=form.cleaned_data['last_name'])
        if form.cleaned_data['first_name']:
            users = users.filter(first_name__icontains=form.cleaned_data['first_name'])
        if form.cleaned_data['sort']:
            users = users.order_by(form.cleaned_data['sort'])
    context = {
        'users': users,
        'form': form
    }
    return render(request, 'main/users_list.html', context)


class UserDetailView(DetailView):
    """
    вывод карточки конретного пользователя
    """
    model = User
    template_name = 'main/user_detail.html'


class UserCreateView(CreateView):
    """
    создание пользователя
    """
    form_class = UserCreateForm
    template_name = 'main/user_create.html'


class UserDeleteView(DeleteView):
    """
    удаление пользователя
    """
    model = User
    template_name = 'main/user_delete.html'
    success_url = reverse_lazy('users_list')


def export_users_to_excel(request):
    """
    экспорт данных о всех пользователях в excel
    """
    users = User.objects.all()
    response = export_to_excel(users)
    return response
