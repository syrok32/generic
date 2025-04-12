from rest_framework import serializers

from info.models import Cours, Lesson, Subscription
from users.models import Payment
from .validators import YouTubeValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [YouTubeValidator(field="desc")]


class CoursSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lesson = LessonSerializer(source="lesson_set", many=True, required=False)
    is_subscribed = serializers.SerializerMethodField()

    def get_lesson_count(self, obj):
        return obj.lesson_set.count()

    class Meta:
        model = Cours
        fields = "__all__"

    def get_is_subscribed(self, obj):
        """Проверяет, подписан ли текущий пользователь на курс"""
        user = self.context.get("request").user
        if user.is_authenticated:
            return Subscription.objects.filter(
                user_fk=user, cuors_fk=obj
            ).exists()
        return False


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        extra_kwargs = {
            "user": {"read_only": True}  # Поле будет автоматически заполняться
        }

    def create(self, validated_data):
        request = self.context.get("request")
        if (
            request and not request.user.is_staff
        ):  # Обычным пользователям user менять нельзя
            validated_data["user"] = request.user
        return super().create(validated_data)
