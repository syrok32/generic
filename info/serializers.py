from rest_framework import serializers

from info.models import Cours, Lesson, Payment


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CoursSerializer(serializers.ModelSerializer):

    lesson_count = serializers.SerializerMethodField()
    lesson = LessonSerializer(source='lesson_set', many=True,)
    def get_lesson_count(self, obj):
        return obj.lesson_set.count()
    class Meta:
        model = Cours
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'