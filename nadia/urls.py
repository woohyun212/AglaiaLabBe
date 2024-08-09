from django.urls import path, include
from nadia.views import UserViewSet
from rest_framework import routers
from .views import PlayerStatsViewSet


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'playerstats', PlayerStatsViewSet, basename='playerstatsmodel')


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    # path('playerstats/<str:nickname>/', PlayerStatsViewSet.as_view({'get': 'retrieve'})),
]
