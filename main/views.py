from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from main.paginators import EducationPaginator
from main.permissions import IsModeratorOrReadOnly, IsCourseOrLessonOwner, IsPaymentOwner, IsCourseOwner

from main.models import Course, Lesson, Payment, Subscription
from main.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer
from users.models import UserRoles


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet для модели обучающего курса"""
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrReadOnly | IsCourseOwner]
    pagination_class = EducationPaginator

    def get_queryset(self):
        """Переопределяем queryset, чтобы доступ к обьекту имели только его владельцы и модератор"""

        if self.request.user.role == UserRoles.MODERATOR:
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """Переопределяем метод создания обьекта с условием, чтобы модераторы не могли создавать обьект"""

        if self.request.user.role == UserRoles.MODERATOR:
            raise PermissionDenied("Вы не можете создавать новые курсы!")
        else:
            new_payment = serializer.save()
            new_payment.owner = self.request.user
            new_payment.save()

    def perform_destroy(self, instance):
        """Переопределяем метод удаления обьекта с условием, чтобы модераторы не могли удалять обьект"""

        if self.request.user.role == UserRoles.MODERATOR:
            raise PermissionDenied("Вы не можете удалять курсы!")
        instance.delete()


class LessonCreateAPIView(generics.CreateAPIView):
    """Generic-класс для создания объекта модели Lesson"""
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrReadOnly | IsCourseOrLessonOwner]

    def perform_create(self, serializer):
        """ Переопределяем метод создания обьекта с условием, чтобы модераторы не могли создавать обьект """

        if self.request.user.role == UserRoles.MODERATOR:
            raise PermissionDenied("Вы не можете создать новый урок!")
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """Generic-класс для просмотра всех объектов Lesson"""
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrReadOnly | IsCourseOrLessonOwner]
    pagination_class = EducationPaginator

    def get_queryset(self):
        """ Переопределяем queryset чтобы доступ к обьекту имели только его владельцы и модератор """

        if self.request.user.role == UserRoles.MODERATOR:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Generic-класс для просмотра одного объекта Lesson"""
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrReadOnly | IsCourseOrLessonOwner]

    def get_queryset(self):
        """ Переопределяем queryset чтобы доступ к обьекту имели только его владельцы и модератор """

        if self.request.user.role == UserRoles.MODERATOR:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Generic-класс для обновления объекта Lesson"""
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrReadOnly | IsCourseOrLessonOwner]

    def get_queryset(self):
        """ Переопределяем queryset чтобы доступ к обьекту имели только его владельцы и модератор """

        if self.request.user.role == UserRoles.MODERATOR:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Generic-класс для удаления одного объекта Lesson"""
    permission_classes = [IsAuthenticated, IsModeratorOrReadOnly | IsCourseOrLessonOwner]

    def get_queryset(self):
        """ Переопределяем queryset чтобы доступ к обьекту имели только его владельцы и модератор """

        if self.request.user.role == UserRoles.MODERATOR:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)

    def perform_destroy(self, instance):
        """ Переопределяем метод удаления обьекта с условием, чтобы модераторы не могли удалять обьект """

        if self.request.user.role == UserRoles.MODERATOR:
            raise PermissionDenied("Вы не можете удалять уроки!")
        instance.delete()


class PaymentListAPIView(generics.ListAPIView):
    """ Generic-класс для вывода списка платежей """

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrReadOnly | IsPaymentOwner]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    # Определяем фильтрацию по нужным нам полям
    filterset_fields = ('course', 'lesson', 'owner', 'payment_method',)
    # Определяем фильтрацию по дате
    ordering_fields = ('payment_date',)

    def get_queryset(self):
        """ Переопределяем queryset чтобы доступ к обьекту имели только его владельцы и модератор """

        if self.request.user.role == UserRoles.MODERATOR:
            return Payment.objects.all()
        else:
            return Payment.objects.filter(owner=self.request.user)


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    """ Generic-класс для просмотра платежа """

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrReadOnly | IsPaymentOwner]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    # Определяем фильтрацию по нужным нам полям
    filterset_fields = ('course', 'lesson', 'owner', 'payment_method',)
    # Определяем фильтрацию по дате
    ordering_fields = ('payment_date',)

    def get_queryset(self):
        """ Переопределяем queryset чтобы доступ к обьекту имели только его владельцы и модератор """

        if self.request.user.role == UserRoles.MODERATOR:
            return Payment.objects.all()
        else:
            return Payment.objects.filter(owner=self.request.user)


class PaymentCreateAPIView(generics.CreateAPIView):
    """ Generic - класс для создания нового платежа """

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsPaymentOwner]

    def perform_create(self, serializer):
        """ Переопределяем метод создания обьекта с условием, чтобы модераторы не могли создавать обьект """

        if self.request.user.role == UserRoles.MODERATOR:
            raise PermissionDenied("Вы не можете создавать новые платежи!")
        else:
            new_payment = serializer.save()
            new_payment.owner = self.request.user
            new_payment.save()


class SubscriptionViewSet(viewsets.ModelViewSet):
    """ ViewSet - набор основных CRUD действий над подписками на курсы """

    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    lookup_field = 'id'

    def perform_create(self, serializer):
        """ Переопределение метода создания подписки, чтобы сохранять текущий статус подписки True или False """

        new_subscription = serializer.save(user=self.request.user)  # Сохраняем связь пользователя
        new_subscription.save()
