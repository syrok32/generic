# Generated by Django 5.1.4 on 2025-03-10 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0007_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='cours',
            name='title',
            field=models.CharField(default=12, max_length=150, verbose_name='название'),
            preserve_default=False,
        ),
    ]
