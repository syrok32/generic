from django.db import models

from Restapimodel import settings


# Create your models here.


class Cours(models.Model):
    title = models.CharField(max_length=150, verbose_name="название")
    img = models.ImageField(verbose_name="картинка", null=True)
    desc = models.TextField(verbose_name="описание")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Пользователь",
    )
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"

    def save(self, *args, **kwargs):
        """Отправляем уведомление подписчикам при обновлении курса"""
        print("ss")
        is_update = self.pk is not None
        super().save(*args, **kwargs)

        if is_update:
            print("ssd")
            from info.tasks import send_course_update_email

            send_course_update_email.delay(self.id)


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name="название")
    desc = models.TextField(verbose_name="описание", null=True)
    img = models.ImageField(verbose_name="картинка", null=True)
    video = models.CharField(max_length=150, verbose_name="ссылка", null=True)
    cours = models.ForeignKey(
        Cours,
        on_delete=models.SET_NULL,
        verbose_name="курс",
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Пользователь",
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"


class Subscription(models.Model):
    cuors_fk = models.ForeignKey(
        Cours,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="подписка-на-курс",
    )
    user_fk = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="подписка-на-курс",
    )

    class Meta:
        verbose_name = "подписка"
        verbose_name_plural = "подписки"
