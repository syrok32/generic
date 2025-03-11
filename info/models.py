from django.db import models

from users.models import User


# Create your models here.


class Cours(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    img = models.ImageField(verbose_name="картинка", null=True)
    desc = models.TextField(verbose_name='описание')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    desc = models.TextField(verbose_name='описание', null=True)
    img = models.ImageField(verbose_name="картинка", null=True)
    video = models.CharField(verbose_name='ссылка', null=True)
    cours = models.ForeignKey(Cours, on_delete=models.SET_NULL, verbose_name='курс', blank=True, null=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = "уроки"


# users/models.py
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата опла")
    paid_course = models.ForeignKey(Cours, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Оплаченный курс")
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Оплаченный урок")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма оплаты")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name="Способ оплаты")
