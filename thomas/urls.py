from django.urls import path, include
from rest_framework import routers
from .views import GameInfoViewSet, get_game_info
from .views import fetch_and_add

router = routers.DefaultRouter()
router.register(r'gameInfo', GameInfoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('fetch-and-add/<str:nickname>/', fetch_and_add, name='fetch_and_add'),
    path('games/<str:nickname>/', get_game_info, name='get_game_info'),
]
