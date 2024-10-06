from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.views import EmployeeListModelViewSet


router_v1 = DefaultRouter()
router_v1.register('employees', EmployeeListModelViewSet, basename='employees')

urlpatterns_v1 = [
    path('', include(router_v1.urls)),
]
