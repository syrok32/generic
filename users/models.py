from django.contrib.auth.models import AbstractUser
from django.db import models

from info.models import Cours, Lesson


# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(verbose_name="email address", unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="phone")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="city")
    avatar = models.ImageField(
        upload_to="avatars/", blank=True, null=True, verbose_name="foto"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователь"


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата опла")
    paid_course = models.ForeignKey(
        Cours,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Оплаченный курс",
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Оплаченный урок",
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Сумма оплаты"
    )
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name="Способ оплаты"
    )
    link_to_payment = models.URLField(max_length=500, null=True, blank=True)
