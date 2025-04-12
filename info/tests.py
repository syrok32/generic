from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from .models import Cours, Subscription


class CoursTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username="admin", email="s@.ru", password="123qwe", is_staff=True
        )
        self.owner_user = User.objects.create_user(
            username="owner", email="owner", password="ownerpass"
        )

        self.course = Cours.objects.create(
            title="Test Course", desc="Test Description", user=self.owner_user
        )

        self.create_url = reverse("info:cors-cr")
        self.list_url = reverse("info:cours-list")
        self.detail_url = reverse(
            "info:cours-ret", kwargs={"pk": self.course.id}
        )
        self.update_url = reverse(
            "info:cours-det", kwargs={"pk": self.course.id}
        )
        self.destroy_url = reverse(
            "info:cours-des", kwargs={"pk": self.course.id}
        )
        self.subscribe_url = reverse("info:sub")

    def test_create_course(self):
        self.client.force_authenticate(user=self.admin_user)

        data = {"title": "New Course", "desc": "New Description"}

        # Отправляем POST-запрос
        response = self.client.post(self.create_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cours.objects.count(), 2)

    def test_list_courses(self):
        self.client.force_authenticate(user=self.owner_user)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_retrieve_course(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Course")

    def test_update_course(self):
        self.client.force_authenticate(user=self.admin_user)

        data = {"title": "Updated Course", "desc": "Updated Description"}

        response = self.client.put(self.update_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Course")

    def test_delete_course(self):
        self.client.force_authenticate(user=self.owner_user)

        response = self.client.delete(self.destroy_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Cours.objects.count(), 0)

    def test_subscribe_to_course(self):
        self.client.force_authenticate(user=self.owner_user)

        data = {"cuors_fk": self.course.id}

        response = self.client.post(self.subscribe_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка добавлена")
        self.assertTrue(
            Subscription.objects.filter(
                user_fk=self.owner_user, cuors_fk=self.course
            ).exists()
        )

    def test_unsubscribe_from_course(self):
        self.client.force_authenticate(user=self.owner_user)

        Subscription.objects.create(
            user_fk=self.owner_user, cuors_fk=self.course
        )

        data = {"cuors_fk": self.course.id}

        response = self.client.post(self.subscribe_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка удалена")
        self.assertFalse(
            Subscription.objects.filter(
                user_fk=self.owner_user, cuors_fk=self.course
            ).exists()
        )
