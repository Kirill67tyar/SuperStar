from django.urls import include, path
from rest_framework.routers import DefaultRouter


router_v1 = DefaultRouter()

# router_v1.register("titles", TitleViewSet, basename="title")
# router_v1.register("genres", GenreViewSet, basename="genre")
# router_v1.register("categories", CategoryViewSet, basename="categorie")
# router_v1.register(
#     r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
# )
# router_v1.register(
#     r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
#     CommentViewSet,
#     basename="comments",
# )
# router_v1.register(r"users", UserModelViewSet, basename="users")

urlpatterns_v1 = [
    path('', include(router_v1.urls)),
]
