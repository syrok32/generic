# Generated by Django 5.1.4 on 2025-03-07 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disc', models.TextField(verbose_name='описание')),
            ],
            options={
                'verbose_name': 'машина',
                'verbose_name_plural': 'машина',
            },
        ),
    ]
