from django.db.models import Q
from django_filters.rest_framework import (BooleanFilter, CharFilter,
                                           FilterSet,
                                           ModelMultipleChoiceFilter)

from employees.models import Team, Employee, Level, Position, Grade, Skill, Competence


class EmployeeFilter(FilterSet):
    employee = ModelMultipleChoiceFilter(
        field_name='name',
        queryset=Employee.objects.all(),
        to_field_name='name',
    )
    team = ModelMultipleChoiceFilter(
        field_name='team__name',
        queryset=Team.objects.all(),
        to_field_name='name',
    )
    position = ModelMultipleChoiceFilter(
        field_name='position__name',
        queryset=Position.objects.all(),
        to_field_name='name',
    )
    grade = ModelMultipleChoiceFilter(
        field_name='grade__name',
        queryset=Grade.objects.all(),
        to_field_name='name',
    )
    skill = ModelMultipleChoiceFilter(
        field_name='levels__skill__name',  # Фильтрация через related field
        queryset=Skill.objects.all(),      # Используем Skill для фильтрации
        to_field_name='name',
    )

    class Meta:
        model = Employee
        fields = [
            'employee',
            'team',
            'position',
        ]
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        querystring = {}
        if 'skill' in self.data:
            querystring['levels__skill__name__in'] = self.data.getlist('skill')
        if 'team' in self.data:
            querystring['team__name__in'] = self.data.getlist('team')
        if 'grade' in self.data:
            querystring['grade__name__in'] = self.data.getlist('grade')
        if 'position' in self.data:
            querystring['position__name__in'] = self.data.getlist('position')
        return queryset.filter(**querystring).distinct()


class TeamFilter(FilterSet):
    team = CharFilter(field_name='name', lookup_expr='in',
                      method='filter_by_name')
    employee = CharFilter(field_name='employees__name',
                          lookup_expr='icontains')
    # employee = ModelMultipleChoiceFilter(
    #     field_name='employees__name',
    #     to_field_name='name',
    #     queryset=Employee.objects.all(),
    #     method='filter_by_employee',
    # )

    class Meta:
        model = Team
        fields = [
            'team',
            'employee',
        ]

    def filter_by_name(self, queryset, name, value):
        team_names = self.request.query_params.getlist('team')
        return queryset.filter(name__in=team_names)

    # def filter_by_employee(self, queryset, name, value):
    #     """
    #     Этот метод фильтрует команды так, чтобы выдавать только те команды, которые
    #     содержат конкретного выбранного сотрудника, а не всех сотрудников.
    #     """
    #     if value:
    #         return queryset.filter(employees__name__in=value).distinct()
    #     return queryset
