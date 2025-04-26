from django.contrib import admin

from info.models import Lesson, Cours, Subscription


# Register your models here.
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    pass


@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    pass


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass
