# Generated by Django 5.0.10 on 2025-04-09 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_payment_link_to_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/', verbose_name='foto'),
        ),
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='city'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='phone'),
        ),
    ]
