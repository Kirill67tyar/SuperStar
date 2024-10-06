from django.db.models import OuterRef, Subquery, Prefetch
from django.db.models.functions import Coalesce
from django.db.models import Max, F
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework import mixins
from django_filters.rest_framework import DjangoFilterBackend

from employees.models import (
    Employee,
    Level,
    Team,
)
from api.v1.filters import EmployeeFilter, TeamFilter
from api.v1.serializers import (
    EmployeeModelSerializer,
    TeamModelSerializer,
)


class EmployeeListModelViewSet(mixins.ListModelMixin,
                               GenericViewSet,):
    http_method_names = [
        'get',
        'options',
    ]
    serializer_class = EmployeeModelSerializer
    queryset = (Employee.objects
                .select_related('position', 'grade'))
    filter_backends = (DjangoFilterBackend,)
    filterset_class = EmployeeFilter
    filterset_fields = (
        'team',
    )

    def get_queryset(self):
        # Подзапрос для получения последней оценки
        latest_scores = Level.objects.filter(
            skill=OuterRef('skill'),
            employee=OuterRef('employee')
        ).order_by('-date').values('score')[:1]

        # Подзапрос для получения предпоследней оценки
        penultimate_scores = Level.objects.filter(
            skill=OuterRef('skill'),
            employee=OuterRef('employee')
        ).order_by('-date').values('score')[1:2]

        # Запрос для получения всех уровней с аннотациями
        skills_with_scores = (
            Level.objects
            .select_related('employee', 'skill')
            .annotate(
                latest_score=Subquery(latest_scores),
                penultimate_score=Coalesce(
                    Subquery(penultimate_scores), 5)
            )
            # # distinct('skill') по идее должно работать на postgres
            # # когда подключим к postgres, код который в сериалайзере
            # # убирает лишние level будет не нужен
            # .distinct('skill')
        )
        return self.queryset.prefetch_related(
            'team',
            Prefetch('levels', queryset=skills_with_scores)
        )


class TeamListModelViewSet(mixins.ListModelMixin,
                           GenericViewSet,):
    queryset = Team.objects.all()
    serializer_class = TeamModelSerializer
    http_method_names = [
        'get',
        'options',
    ]
    filter_backends = [DjangoFilterBackend,]
    filterset_class = TeamFilter

    def get_queryset(self):
        # Подзапрос для получения последней оценки
        latest_scores = Level.objects.filter(
            skill=OuterRef('skill'),
            employee=OuterRef('employee')
        ).order_by('-date').values('score')[:1]

        # Подзапрос для получения предпоследней оценки
        penultimate_scores = Level.objects.filter(
            skill=OuterRef('skill'),
            employee=OuterRef('employee')
        ).order_by('-date').values('score')[1:2]

        # Запрос для получения всех уровней с аннотациями
        skills_with_scores = (
            Level.objects
            .select_related(
                'employee',
                'skill',
                'skill__competence',
            )
            .annotate(
                latest_score=Subquery(latest_scores),
                penultimate_score=Coalesce(
                    Subquery(penultimate_scores), 5)
            )
        )
        team_members = Employee.objects.select_related('position', 'grade').prefetch_related(
            'team',
            Prefetch('levels', queryset=skills_with_scores)
        )
        return self.queryset.prefetch_related(
            Prefetch(
                'employees',
                queryset=team_members,
            )
        )
