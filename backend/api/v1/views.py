from rest_framework.response import Response
from django.db.models import OuterRef, Subquery, Prefetch, Q, Count
from django.db.models.functions import Coalesce
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework import mixins
from django_filters.rest_framework import DjangoFilterBackend


from trainings.models import (
    TrainigRequest,
    Level,
    PositionRequirement,
)
from employees.models import (
    Employee,
    Team,
    Position,
    Grade
)
from skills.models import Competence, Skill
from api.v1.pagination import CustomTeamPagination
from api.v1.filters import EmployeeFilter, TrainigRequestFilter
from api.v1.serializers import (
    EmployeeModelSerializer,
    TrainigRequestReadSerializer,
    FilterTeamModelSerializer,
    FilterEmployeeModelSerializer,
    FilterPositionModelSerializer,
    FilterGradeModelSerializer,
    FilterCompetenceModelSerializer,
    FilterSkillModelSerializer,
    FilterTrainigRequestModelSerializer,
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
            .prefetch_related(
                'team',
                'development_requests',
                'ratings',
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


class TeamFilterReadOnly(mixins.ListModelMixin,
                         GenericViewSet,):
    serializer_class = FilterTeamModelSerializer
    http_method_names = [
        'get',
        'options',
    ]
    queryset = Team.objects.all()


class EmployeeFilterReadOnly(mixins.ListModelMixin,
                             GenericViewSet,):
    serializer_class = FilterEmployeeModelSerializer
    http_method_names = [
        'get',
        'options',
    ]
    queryset = Employee.objects.all()


class PositionFilterReadOnly(mixins.ListModelMixin,
                             GenericViewSet,):
    serializer_class = FilterPositionModelSerializer
    http_method_names = [
        'get',
        'options',
    ]
    queryset = Position.objects.all()


class GradeFilterReadOnly(mixins.ListModelMixin,
                          GenericViewSet,):
    serializer_class = FilterGradeModelSerializer
    http_method_names = [
        'get',
        'options',
    ]
    queryset = Grade.objects.all()


class CompetenceFilterReadOnly(mixins.ListModelMixin,
                               GenericViewSet,):
    serializer_class = FilterCompetenceModelSerializer
    http_method_names = [
        'get',
        'options',
    ]
    queryset = Competence.objects.all()


class SkillFilterReadOnly(mixins.ListModelMixin,
                          GenericViewSet,):
    serializer_class = FilterSkillModelSerializer
    http_method_names = [
        'get',
        'options',
    ]
    queryset = Skill.objects.all()


class TrainigRequestFilterReadOnly(mixins.ListModelMixin,
                                   GenericViewSet,):
    serializer_class = FilterTrainigRequestModelSerializer
    queryset = TrainigRequest.objects.all()
    http_method_names = [
        'get',
        'options',
    ]


class ThinTeamReadOnly(mixins.ListModelMixin,
                       GenericViewSet,):
    serializer_class = ThinTeamModelSerializer
    http_method_names = [
        'get',
        'options',
    ]
    queryset = Team.objects.all()


class CompetenceModelViewSet(ModelViewSet):
    # serializer_class = ThinTeamModelSerializer
    http_method_names = [
        'get',
        'options',
    ]
    queryset = Competence.objects.all()
    """
    По выборке берём компетенции и смотрим в таблице Level, суммируем скиллы относящиеся к этой компетенции, 
    в зависимости от выбранной даты (от и до), и делим на количество. Всё это выбирается по выборке, которая фильтруется.
    Насчёт даты, то суммировать надо по месяцам. Если взят сентябрь, даже 30, то он берётся весь.
    """
    pass
