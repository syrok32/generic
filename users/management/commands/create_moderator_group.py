from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from users.models import User  # Замените на вашу модель пользователя

class Command(BaseCommand):
    help = "Создает группу 'Модераторы' с необходимыми разрешениями"

    def handle(self, *args, **kwargs):
        moderator_group, created = Group.objects.get_or_create(name="moders")

        permissions = Permission.objects.filter(
            content_type__model='user'
        )

        # Добавляем разрешения группе
        moderator_group.permissions.set(permissions)

        if created:
            self.stdout.write(self.style.SUCCESS("Группа 'Модераторы' успешно создана"))
        else:
            self.stdout.write(self.style.SUCCESS("Группа 'Модераторы' уже существует"))
