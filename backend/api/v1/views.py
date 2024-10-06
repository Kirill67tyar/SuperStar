from django.db.models import OuterRef, Subquery, Prefetch
from django.db.models.functions import Coalesce
from django.db.models import Max, F
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework import mixins

from employees.models import Employee, Level
from api.v1.serializers import (
    EmployeeModelSerializer,
)


class EmployeeListModelViewSet(mixins.ListModelMixin,
                               GenericViewSet,):
    http_method_names = [
        'get',
        'options',
    ]
    serializer_class = EmployeeModelSerializer
    queryset = (Employee.objects
                .select_related('position', 'grade')
                # .prefetch_related('team', 'levels', 'levels__skill')
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
        skills_with_scores = Level.objects.select_related('employee', 'skill').annotate(
            latest_score=Subquery(latest_scores),
            penultimate_score=Coalesce(Subquery(penultimate_scores), 5)
        ).distinct('skill')
        return self.queryset.prefetch_related(
            'team',
            Prefetch('levels', queryset=skills_with_scores)
        )


    #     """
    #  # Получаем последнее значение score для каждого скилла
    # latest_level = Level.objects.filter(
    #     employee=OuterRef('pk'),  # используем 'pk' для ссылки на Employee
    #     skill=OuterRef('pk')
    # ).order_by('-date').values('score')[:1]

    # # Получаем предпоследнее значение score для каждого скилла
    # previous_level = Level.objects.filter(
    #     employee=OuterRef('pk'),  # используем 'pk' для ссылки на Employee
    #     skill=OuterRef('pk')
    # ).order_by('-date').values('score')[1:2]

    # # Агрегируем данные по последней и предпоследней оценке скилла
    # employees = Employee.objects.annotate(
    #     latest_score=Subquery(latest_level),
    #     previous_score=Coalesce(Subquery(previous_level), 0),
    # ).prefetch_related('levels')  # Предварительная загрузка уровней

    #     # growth=F('latest_score') > F('previous_score')
    #     """
        # pass
