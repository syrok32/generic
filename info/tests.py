from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch

from users.models import User
from .models import Cours, Subscription


class CoursTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="adminpass",
            is_staff=True,
        )
        self.owner_user = User.objects.create_user(
            username="owner", email="owner@example.com", password="ownerpass"
        )
        self.regular_user = User.objects.create_user(
            username="regular", email="regular@example.com", password="regularpass"
        )

        self.course = Cours.objects.create(
            title="Test Course", desc="Test Description", user=self.owner_user
        )

        # URL endpoints
        self.create_url = reverse("info:cors-cr")
        self.list_url = reverse("info:cours-list")
        self.detail_url = reverse("info:cours-ret", kwargs={"pk": self.course.id})
        self.update_url = reverse("info:cours-det", kwargs={"pk": self.course.id})
        self.destroy_url = reverse("info:cours-des", kwargs={"pk": self.course.id})
        self.subscribe_url = reverse("info:sub")

    @patch("info.tasks.send_course_update_email.delay")
    def test_create_course(self, mock_celery):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "title": "New Course",
            "desc": "New Description",
            "user": self.owner_user.id,
        }

        response = self.client.post(self.create_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cours.objects.count(), 2)
        self.assertEqual(response.data["title"], "New Course")
        mock_celery.assert_not_called()  # При создании письмо не отправляется

    def test_list_courses(self):
        # Создаем еще один курс для проверки
        Cours.objects.create(title="Second Course", desc="Desc", user=self.owner_user)

        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["title"], "Test Course")

    def test_retrieve_course(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Course")
        self.assertEqual(response.data["desc"], "Test Description")

    @patch("info.tasks.send_course_update_email.delay")
    def test_update_course(self, mock_celery):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "title": "Updated Course",
            "desc": "Updated Description",
            "user": self.owner_user.id,
        }

        response = self.client.put(self.update_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, "Updated Course")
        self.assertEqual(self.course.desc, "Updated Description")
        mock_celery.assert_called_once_with(self.course.id)

    def test_delete_course_by_owner(self):
        self.client.force_authenticate(user=self.owner_user)
        response = self.client.delete(self.destroy_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Cours.objects.count(), 0)

    def test_delete_course_by_non_owner(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.delete(self.destroy_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Cours.objects.count(), 1)

    def test_subscribe_to_course(self):
        self.client.force_authenticate(user=self.regular_user)
        data = {"cuors_fk": self.course.id}

        response = self.client.post(self.subscribe_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка добавлена")
        self.assertTrue(
            Subscription.objects.filter(
                user_fk=self.regular_user, cuors_fk=self.course
            ).exists()
        )

    def test_unsubscribe_from_course(self):
        # Сначала создаем подписку
        Subscription.objects.create(user_fk=self.regular_user, cuors_fk=self.course)

        self.client.force_authenticate(user=self.regular_user)
        data = {"cuors_fk": self.course.id}

        response = self.client.post(self.subscribe_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка удалена")
        self.assertFalse(
            Subscription.objects.filter(
                user_fk=self.regular_user, cuors_fk=self.course
            ).exists()
        )

    def test_subscribe_to_nonexistent_course(self):
        self.client.force_authenticate(user=self.regular_user)
        data = {"cuors_fk": 999}  # Несуществующий ID

        response = self.client.post(self.subscribe_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)
