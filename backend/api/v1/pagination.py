from collections import OrderedDict
from django.http import Http404
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.utils.urls import remove_query_param, replace_query_param

from employees.models import Team, Employee
from api.v1.serializers import EmployeeModelSerializer


class CustomTeamPagination(PageNumberPagination):
    page_size = None  # Размер страницы будет зависеть от числа сотрудников в команде
    page_query_param = 'team'

    def paginate_queryset(self, queryset, request, view=None):
        self.teams_list = list(
            map(
                int,
                Team.objects.values_list('pk', flat=True)
            )
        )
        team_pk = request.query_params.get('team', None)
        if (team_pk) and (team_pk.isdigit()) and (int(team_pk) in self.teams_list):
            current_team = get_object_or_404(Team, pk=int(team_pk))
            team_pk = current_team.pk
        else:
            team_pk = self.teams_list[0]
        current_team_employees = queryset.filter(team__pk=team_pk)
        self.request = request
        self.team = team_pk
        self.current_team_employees = current_team_employees
        return list(self.current_team_employees)

    def get_paginated_response(self, data):
        return Response(data)

    def get_html_context(self):
        return {}
