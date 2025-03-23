from django.db import models

from Restapimodel import settings


# Create your models here.


class Cours(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    img = models.ImageField(verbose_name="картинка", null=True)
    desc = models.TextField(verbose_name='описание')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,null=True, blank=True, verbose_name="Пользователь")

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    desc = models.TextField(verbose_name='описание', null=True)
    img = models.ImageField(verbose_name="картинка", null=True)
    video = models.CharField(max_length=150, verbose_name='ссылка', null=True)
    cours = models.ForeignKey(Cours, on_delete=models.SET_NULL, verbose_name='курс', blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Пользователь")
    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = "уроки"

class Subscription(models.Model):
    cuors_fk = models.ForeignKey(Cours, on_delete=models.CASCADE, null=True, verbose_name='подписка-на-курс')
    user_fk = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, verbose_name='подписка-на-курс')

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
