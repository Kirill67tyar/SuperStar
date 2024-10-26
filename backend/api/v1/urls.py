from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.views import (
    EmployeeListModelViewSet,
    EmployeeListModelViewSet,
    TrainigRequestView,
    TeamFilterReadOnly,
    EmployeeFilterReadOnly,
    PositionFilterReadOnly,
    GradeFilterReadOnly,
    CompetenceFilterReadOnly,
    SkillFilterReadOnly,
    TrainigRequestFilterReadOnly,
    ThinTeamReadOnly,
    AverageScoreByDateView,
)


router_v1 = DefaultRouter()
router_v1.register('employees', EmployeeListModelViewSet, basename='employees')
router_v1.register('trainig_requests', TrainigRequestView, basename='trainig_requests')
router_v1.register('teams-list', ThinTeamReadOnly, basename='teams-list')

filter_router = DefaultRouter()
filter_router.register('teams', TeamFilterReadOnly, basename='teams')
filter_router.register('employees_filters', EmployeeFilterReadOnly, basename='employees_filters')
filter_router.register('positions', PositionFilterReadOnly, basename='positions')
filter_router.register('grades', GradeFilterReadOnly, basename='grades')
filter_router.register('competences', CompetenceFilterReadOnly, basename='competences')
filter_router.register('skills', SkillFilterReadOnly, basename='skills')
filter_router.register('data', TrainigRequestFilterReadOnly, basename='data')


urlpatterns_v1 = [
    path('', include(router_v1.urls)),
    path('filters/', include(filter_router.urls)),
    path('rating-dynamics/', AverageScoreByDateView.as_view(), name='rating-dynamics'),
]
