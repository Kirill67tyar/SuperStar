from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.views import (
    EmployeeListModelViewSet,
    TeamListModelViewSet,
    TrialEmployeeListModelViewSet,
    TrainigRequestView,
)


router_v1 = DefaultRouter()
router_v1.register('employees', TrialEmployeeListModelViewSet, basename='employees')
router_v1.register('trainig_requests', TrainigRequestView, basename='trainig_requests')

urlpatterns_v1 = [
    path('', include(router_v1.urls)),
]
