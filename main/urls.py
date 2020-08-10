from django.urls import path

from .views import list_users, UserDetailView, UserCreateView, UserDeleteView, export_users_to_excel, \
    poll_view, ScoresListView, ScoreDetailView

urlpatterns = [
    path('', list_users, name='users_list'),
    path('create/', UserCreateView.as_view(), name='user_create'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
    path('export/', export_users_to_excel, name='export'),

    path('poll/', poll_view, name='poll'),
    path('api/score/<int:pk>/', ScoreDetailView.as_view(), name='score_detail'),
    path('api/score/', ScoresListView.as_view(), name='scores_list'),
    # path('api/users/<int:pk>/', api_user_detail),
    # path('api/users/', api_users),
]
