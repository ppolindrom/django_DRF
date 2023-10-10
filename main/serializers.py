from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from main.models import Course, Lesson, Payment, Subscription
from main.validators import LinkValidator
from users.models import User


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели уроков"""

    course = SlugRelatedField(slug_field='name', queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [
            LinkValidator(fields=['name', 'description', 'video_url']),
            serializers.UniqueTogetherValidator(fields=['name', 'description'], queryset=Lesson.objects.all())
        ]


class LessonListSerializer(serializers.ModelSerializer):
    """Сериализотор для модели урока для использования его в выводе в курсах"""

    class Meta:
        model = Lesson
        fields = ['id', 'name', 'description', 'preview', 'video_url']


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели курсов"""

    # Выводим счетчик уроков
    lessons_count = serializers.IntegerField(source='lesson_set.count', read_only=True)
    # Расширяем сериализатор дополнительным вложенным полем с уроками
    lessons = serializers.SerializerMethodField()

    # Выводим имя пользователя в поле "owner", вместо цифры
    owner = SlugRelatedField(slug_field='first_name', queryset=User.objects.all())

    class Meta:
        model = Course
        fields = '__all__'
        validators = [
            LinkValidator(fields=['name', 'description']),
            serializers.UniqueTogetherValidator(fields=['name', 'description'], queryset=Course.objects.all())
        ]

    # Получаем все поля для дополнительного поля уроков с фильтрацией по курсу
    def get_lessons(self, course):
        return LessonListSerializer(Lesson.objects.filter(course=course), many=True).data

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return Subscription.objects.filter(user=user, course=obj).exists()


class PaymentSerializer(serializers.ModelSerializer):
    """ Сериализотор для модели платежей """

    course = SlugRelatedField(slug_field='name', queryset=Course.objects.all())
    lesson = SlugRelatedField(slug_field='name', queryset=Lesson.objects.all())
    owner = SlugRelatedField(slug_field='email', queryset=User.objects.all())

    class Meta:
        model = Payment
        fields = '__all__'


class PaymentForOwnerSerializer(serializers.ModelSerializer):
    """ Сериализотор для модели платежей для использования его в выводе у пользователей """

    class Meta:
        model = Payment
        fields = ['id', 'amount', 'payment_date', 'payment_method']


class SubscriptionSerializer(serializers.ModelSerializer):
    """ Сериализотор для модели подписки пользователя на курс """

    class Meta:
        model = Subscription
        fields = '__all__'
