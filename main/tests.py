from datetime import date

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class UserScoreAPITests(APITestCase):
    """
    тесты для проверки API голосования
    """

    def setUp(self):
        User.objects.create(id=1,
                            last_name='Иванов',
                            first_name='Иван',
                            date_of_birth=date(1990, 10, 10),
                            photo='photos/ivanov.jpg',
                            score=8
                            )

        User.objects.create(id=2,
                            last_name='Петров',
                            first_name='Петр',
                            date_of_birth=date(1991, 11, 11),
                            photo='photos/petrov.jpg',
                            score=5
                            )
        self.users = User.objects.all()

    def test_users_created(self):
        """
        создались ли пользовали
        """
        self.assertEqual(User.objects.count(), 2)

    def test_scores_list_retrieve(self):
        """
        загрузка списка со счетом каждого пользователя
        """
        response = self.client.get(reverse('scores_list'))
        expected_output = [
            {"id": 1, "score": 8},
            {"id": 2, "score": 5}
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_output)

    def test_score_detail_retrieve(self):
        """
        загрузка счета конкретного пользователя
        """
        response = self.client.get(reverse("score_detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 1, 'score': 8})

    def test_score_detail_update(self):
        """
        обновление счета конкретного пользователя, и проверка что он не превышает максимального
        """
        data = {"id": "1", 'score': 0}
        response = self.client.put(reverse("score_detail", kwargs={"pk": 1}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 1, 'score': 9})
        response_2 = self.client.put(reverse("score_detail", kwargs={"pk": 1}))
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(response_2.data, {'id': 1, 'score': 10})
        response_3 = self.client.put(reverse("score_detail", kwargs={"pk": 1}))
        self.assertEqual(response_3.status_code, status.HTTP_200_OK)
        self.assertEqual(response_3.data, {'id': 1, 'score': 10})
