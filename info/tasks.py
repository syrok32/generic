from celery import shared_task
from django.core.mail import send_mail

from Restapimodel.settings import DEFAULT_FROM_EMAIL

from django.apps import apps
@shared_task
def send_course_update_email(course_id):
    print('ee')
    Cours = apps.get_model('info', 'Cours')  # 🔹 Динамически загружаем модель
    Subscription = apps.get_model('info', 'Subscription')
    course = Cours.objects.get(id=course_id)
    subject = f"Обновление курса: {course.title}"
    message = f"Курс '{course.title}' был обновлён! Проверьте новые материалы на платформе."
    print('fff')
    from_email = DEFAULT_FROM_EMAILa

    # Получаем email всех подписчиков курса
    subscribers = Subscription.objects.filter(cuors_fk=course).select_related("user_fk")
    recipient_list = [sub.user_fk.email for sub in subscribers]

    if recipient_list:
        print('send')
        send_mail(subject, message, from_email, recipient_list)
