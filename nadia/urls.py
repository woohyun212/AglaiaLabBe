from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, PlayerViewSet, PlayerStatsViewSet, MMRHistoryViewSet, CharacterStatsViewSet
from .views import register_player

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'players', PlayerViewSet)
router.register(r'player-stats', PlayerStatsViewSet)
router.register(r'mmr-history', MMRHistoryViewSet)
router.register(r'character-stats', CharacterStatsViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('register/<str:nickname>/', register_player, name='register_player'),
]
