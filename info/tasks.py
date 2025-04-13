from celery import shared_task
from django.core.mail import send_mail
from django.apps import apps
from Restapimodel.settings import DEFAULT_FROM_EMAIL
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def send_course_update_email(self, course_id):
    """
    Отправляет уведомления об обновлении курса подписчикам
    Args:
        course_id (int): ID курса для отправки уведомлений
    """
    if course_id is None:
        logger.error("Не указан course_id!")
        return
    try:
        logger.info(f"Начало отправки уведомлений для курса {course_id}")

        # Динамически загружаем модели
        Cours = apps.get_model("info", "Cours")
        Subscription = apps.get_model("info", "Subscription")

        # Получаем курс с обработкой случая отсутствия
        try:
            course = Cours.objects.get(id=course_id)
        except Cours.DoesNotExist as e:
            logger.error(f"Курс с ID {course_id} не найден: {str(e)}")
            return

        # Формируем email данные
        subject = f"Обновление курса: {course.title}"
        message = f"Курс '{course.title}' был обновлён! Проверьте новые материалы на платформе."

        # Оптимизированный запрос для получения email подписчиков
        recipient_list = Subscription.objects.filter(cuors_fk=course).values_list(
            "user_fk__email", flat=True
        )

        if not recipient_list:
            logger.info(f"Нет подписчиков для курса {course_id}")
            return

        # Отправка email
        send_mail(
            subject=subject,
            message=message,
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=list(recipient_list),
            fail_silently=False,
        )

        logger.info(
            f"Успешно отправлено {len(recipient_list)} уведомлений для курса {course_id}"
        )

    except Exception as e:
        logger.error(f"Ошибка при отправке уведомлений для курса {course_id}: {str(e)}")
        # Повторная попытка через 5 минут
        raise self.retry(exc=e, countdown=300)
