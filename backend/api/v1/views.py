from rest_framework import status
from rest_framework.response import Response
from django.db.models import OuterRef, Subquery, Prefetch, Q, Count
from django.db.models.functions import Coalesce
from django.db.models import Max, F
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework import mixins
from django_filters.rest_framework import DjangoFilterBackend
from itertools import groupby


from trainings.models import (
    TrainigRequest,
    Level,
    PositionRequirement,
)
from employees.models import (
    Employee,
    Team,
)
from api.v1.pagination import CustomTeamPagination
from api.v1.filters import EmployeeFilter, TeamFilter, TrainigRequestFilter
from api.v1.serializers import (
    EmployeeModelSerializer,
    TeamModelSerializer,
    TeamGroupedSerializer,
    TrainigRequestReadSerializer,
    ThinTeamModelSerializer,
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
        # self.request.query_params
        # Подзапрос для получения последней оценки
        a = 1
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
        # ! =-=-=-=-=
        # position_requirement_subquery = PositionRequirement.objects.filter(
        #         Q(position=OuterRef('position')) & Q(grade=OuterRef('grade'))
        #         ).values('skill', 'score')
        # position_requirement_subquery = PositionRequirement.objects.filter(
        #     Q(position=OuterRef('position')) & Q(grade=OuterRef('grade'))
        # )
        # ! =-=-=-=-=
        team_members = (
            Employee.objects
            .select_related('position', 'grade')
            .prefetch_related(
                'team',
                # 'position__requirements_position',  # или такой вариант
                Prefetch('levels', queryset=skills_with_scores),
                # Prefetch('position__requirements_position', queryset=position_requirement_subquery, to_attr='position_requirements')
            )
            # .annotate(
            #     position_requirements=Subquery(
            #         position_requirements_subquery
            #         # .values('id')
            #     )
            # )
        )
        # team_members = Employee.objects.select_related('position', 'grade').prefetch_related(
        #     'team',
        #     Prefetch('levels', queryset=skills_with_scores)
        # )
        return self.queryset.prefetch_related(
            Prefetch(
                'employees',
                queryset=team_members,
            )
        )
    # def get_queryset(self):
    #     # self.request.query_params
    #     # Подзапрос для получения последней оценки
    #     a = 1
    #     latest_scores = Level.objects.filter(
    #         skill=OuterRef('skill'),
    #         employee=OuterRef('employee')
    #     ).order_by('-date').values('score')[:1]

    #     # Подзапрос для получения предпоследней оценки
    #     penultimate_scores = Level.objects.filter(
    #         skill=OuterRef('skill'),
    #         employee=OuterRef('employee')
    #     ).order_by('-date').values('score')[1:2]

    #     # Запрос для получения всех уровней с аннотациями
    #     skills_with_scores = (
    #         Level.objects
    #         .select_related(
    #             'employee',
    #             'skill',
    #             'skill__competence',
    #         )
    #         .annotate(
    #             latest_score=Subquery(latest_scores),
    #             penultimate_score=Coalesce(
    #                 Subquery(penultimate_scores), 5)
    #         )
    #     )
    #     # ! =-=-=-=-=
    #     # position_requirement_subquery = PositionRequirement.objects.filter(
    #     #         Q(position=OuterRef('position')) & Q(grade=OuterRef('grade'))
    #     #         ).values('skill', 'score')
    #     position_requirement_subquery = PositionRequirement.objects.filter(
    #         Q(position=OuterRef('position')) & Q(grade=OuterRef('grade'))
    #     )
    #     # ! =-=-=-=-=
    #     team_members = (
    #         Employee.objects
    #         .select_related('position', 'grade')
    #         .prefetch_related(
    #             'team',
    #             # 'position__requirements_position',  # или такой вариант
    #             Prefetch('levels', queryset=skills_with_scores),
    #             # Prefetch('position__requirements_position', queryset=position_requirement_subquery, to_attr='position_requirements')
    #         )
    #         # .annotate(
    #         #     position_requirements=Subquery(
    #         #         position_requirements_subquery
    #         #         # .values('id')
    #         #     )
    #         # )
    #     )
    #     # team_members = Employee.objects.select_related('position', 'grade').prefetch_related(
    #     #     'team',
    #     #     Prefetch('levels', queryset=skills_with_scores)
    #     # )
    #     return self.queryset.prefetch_related(
    #         Prefetch(
    #             'employees',
    #             queryset=team_members,
    #         )
    #     )


# class TrialEmployeeListModelViewSet(mixins.ListModelMixin,
#                                     GenericViewSet,):
class TrialEmployeeListModelViewSet(ModelViewSet):
    http_method_names = [
        'get',
        'options',
    ]
    serializer_class = EmployeeModelSerializer
    queryset = (Employee.objects
                .select_related(
                    'position',
                    'grade'
                )
                )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = EmployeeFilter
    pagination_class = CustomTeamPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        requirements_for_position = PositionRequirement.objects.select_related(
            'position',
            'grade',
            'skill',
        ).values(
            'position__name',
            'grade__name',
            'skill__name',
            'score'
        )
        requirement_data = {}

        for p in requirements_for_position:

            requirement_data[p['position__name']] = (
                requirement_data
                .get(p['position__name'], {})
            )
            requirement_data[p['position__name']][p['grade__name']] = (
                requirement_data
                [p['position__name']]
                .get(p['grade__name'], {})
            )
            (requirement_data
             [p['position__name']]
             [p['grade__name']]
             .update({p['skill__name']: p['score']}))
        context['requirement_data'] = requirement_data
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        # Подзапрос для получения последних и предпоследних уровней
        latest_levels = Level.objects.filter(
            skill=OuterRef('skill'),
            employee=OuterRef('employee')
        ).order_by('-date').values('date')[:1]

        penultimate_levels = Level.objects.filter(
            skill=OuterRef('skill'),
            employee=OuterRef('employee')
        ).order_by('-date').values('date')[1:2]

        # Запрос для получения уровней с аннотациями
        skills_with_scores = (
            Level.objects
            .filter(
                Q(date=Subquery(latest_levels)) | Q(
                    date=Subquery(penultimate_levels))
            )
            .select_related(
                'skill',
                'skill__competence',
            )
            .annotate(
                latest_score=Subquery(
                    Level.objects.filter(
                        skill=OuterRef('skill'),
                        employee=OuterRef('employee'),
                        date=Subquery(latest_levels)
                    ).values('score')[:1]
                ),
                penultimate_score=Coalesce(
                    Subquery(
                        Level.objects.filter(
                            skill=OuterRef('skill'),
                            employee=OuterRef('employee'),
                            date=Subquery(penultimate_levels)
                        ).values('score')[:1]
                    ), 1
                )
            )
        )

        # Запрос для получения сотрудников с предустановленными уровнями
        queryset = (
            queryset
            # .select_related('position', 'grade')
            .prefetch_related(
                'team',
                'development_requests',
                Prefetch('levels', queryset=skills_with_scores,
                         to_attr='filtered_levels')
            )
            .annotate(
                quantity_requests=Count('training_requests__id')
            )
        )
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        team = request.query_params.get('team', None)
        if team:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(
                    page,
                    many=True,
                    context=self.get_serializer_context()
                )
                return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(
            queryset,
            many=True,
            context=self.get_serializer_context()
        )
        return Response(serializer.data)

    # def list(self, request, *args, **kwargs):
    #     # Получаем всех сотрудников с учётом фильтров и предвыборкой команд
    #     employees = self.filter_queryset(
    #         self.get_queryset()  # Оптимизация для избежания n+1 проблемы
    #     )
    #     # employees = self.get_queryset()  # Оптимизация для избежания n+1 проблемы

    #     # Получаем все уникальные команды, к которым относятся сотрудники
    #     # teams = Team.objects.prefetch_related('employees').filter(employees__in=employees).distinct()
    #     teams = (
    #         Team.objects
    #         .prefetch_related(
    #             Prefetch(
    #                 'employees',
    #                 queryset=employees,
    #             )
    #         )
    #         .filter(employees__in=employees)
    #         .distinct()
    #     )

    #     # Сериализуем данные по командам, передавая сотрудников через context
    #     serializer = TeamGroupedSerializer(
    #         teams,
    #         many=True,
    #         context={'employees': employees})
    #     return Response(
    #         serializer.data,
    #         status=status.HTTP_200_OK
    #         )


class TrainigRequestView(ModelViewSet):
    queryset = (TrainigRequest.objects
                .select_related(
                    'employee',
                    'employee__position',
                    'employee__grade',
                    'skill',
                    'skill__competence'
                    ).all())
    serializer_class = TrainigRequestReadSerializer
    http_method_names = ['get', ]
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TrainigRequestFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        skill_requests = []
        for item in data:
            skill_name = item['skill']['name']
            skill_data = {
                'name': skill_name,
                'competence': item['skill']['competence'],
                'course': item['skill']['skill_course'],
                'quantity_employees': len(item['skill']['employees']),
                'employees': item['skill']['employees']
            }
            skill_requests.append(skill_data)

        response_data = {
            'request_count': queryset.count(),
            'results': skill_requests,
        }

        return Response(response_data)

# # для второго варианта сериализатора
#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         serializer = self.get_serializer(queryset, many=True)
#         data = serializer.data
#         skill_requests = {}
#         for item in data:
#             skill_name = item['skill']['name']
#             if skill_name not in skill_requests:
#                 skill_requests[skill_name] = []
#             skill_requests[skill_name].append(item)
#         response_data = {
#             'request_count': queryset.count(),
#             'results': skill_requests
#         }

#         return Response(response_data)


class ThinTeamReadOnly(ReadOnlyModelViewSet):
    serializer_class = ThinTeamModelSerializer
    http_method_names = [
        'get',
        'options',
    ]
    queryset = Team.objects.all()