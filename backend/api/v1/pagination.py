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
        teams = request.query_params.get('teams_list', '')
        if teams:
            teams_list = list(map(int, filter(lambda x: x.isdigit(), teams.split(','))))
        else:
            teams_list = []
        if teams_list:
            existing_teams = (
                list(
                    Team.objects
                    .filter(pk__in=teams_list)
                    .values_list('pk', flat=True)
                )
            )
            if set(existing_teams) != set(teams_list):
                raise NotFound("Not valid teams")
            self.teams_list = teams_list
        else:
            self.teams_list = list(map(int, Team.objects.values_list('pk', flat=True)))
        team_pk = request.query_params.get('team', None)
        if (team_pk) and (team_pk.isdigit()) and (int(team_pk) in self.teams_list):
            current_team = get_object_or_404(Team, pk=int(team_pk))
            # raise NotFound("Team not found")
            team_pk = current_team.pk
        else:
            team_pk = self.teams_list[0]
        current_team_employees = queryset.filter(team__pk=team_pk)
        self.request = request
        self.team = team_pk
        self.current_team_employees = current_team_employees
        return list(self.current_team_employees)

    def get_paginated_response(self, data):
        
        return Response(OrderedDict([
                # ('count', self.page.paginator.count),
                # ('next', self.get_next_link()),
                # ('previous', self.get_previous_link()),
                ('team', self.team),
                ('teams_list', self.teams_list if data else []),
                ('count', self.current_team_employees.count()),
                ('results', data)
            ]))
        # return Response({
        #     'links': {
        #         'next': self.get_next_link(),
        #         'previous': self.get_previous_link(),
        #     },
        #     'current_team': self.team,
        #     'count': self.current_team_employees.count(),
        #     'employees': EmployeeModelSerializer(self.current_team_employees, many=True).data,
        # })
    

    # def get_next_link(self):
    #     # Логика для определения следующей команды
    #     team = self.request.query_params.get('team', '')
    #     if team.isdigit() and int(team) in self.teams_list:
    #         team = int(team)
    #         current_index = self.teams_list.index(team)
    #     else:
    #         current_index = -1
        
    #     next_index = current_index + 1
        
    #     if next_index < len(self.teams_list):
    #         url = self.request.build_absolute_uri()
    #         return replace_query_param(url, self.page_query_param, self.teams_list[next_index])
    #         # return f"?teams_list={','.join(self.teams_list)}&team={self.teams_list[next_index]}"
    #     else:
    #         return None

    # def get_previous_link(self):
    #     team = self.request.query_params.get('team', '')
    #     if team.isdigit() and int(team) in self.teams_list:
    #         team = int(team)
    #         current_index = self.teams_list.index(team)
    #     else:
    #         current_index = -1
        
    #     previous_index = current_index - 1
        
    #     if previous_index >= 0:
    #         url = self.request.build_absolute_uri()
    #         return replace_query_param(url, self.page_query_param, self.teams_list[previous_index])
    #         # return f"?teams_list={','.join(self.teams_list)}&page={self.teams_list[previous_index]}"
    #     else:
    #         return None
        
    def get_html_context(self):
        return {}