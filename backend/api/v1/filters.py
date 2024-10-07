from django_filters.rest_framework import (BooleanFilter, CharFilter,
                                           FilterSet,
                                           ModelMultipleChoiceFilter)

from employees.models import Team, Employee


class EmployeeFilter(FilterSet):

    team = ModelMultipleChoiceFilter(
        field_name='team__name',
        to_field_name='name',
        queryset=Team.objects.all(),
    )

    class Meta:
        model = Employee
        fields = [
            'team',
        ]

class TeamFilter(FilterSet):
    team = CharFilter(field_name='name', lookup_expr='in', method='filter_by_name')

    class Meta:
        model = Team
        fields = ['team']

    def filter_by_name(self, queryset, name, value):
        team_names = self.request.query_params.getlist('team')
        return queryset.filter(name__in=team_names)