# Generated by Django 5.1.4 on 2025-03-13 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0009_delete_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='video',
            field=models.CharField(max_length=150, null=True, verbose_name='ссылка'),
        ),
    ]
