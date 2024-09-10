from rest_framework import viewsets, status
from .serializers import *

from bser_api import BserAPI
from AglaiaLabBE.settings.base import ER_API_KEY

# BserAPI Instance
ER = BserAPI(ER_API_KEY)
CURRENT_SEASON = 27


# user view set  ###########
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


######################################
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .serializers import *
from thomas.models import BattleRecord
from django.db.models import Sum, Avg
from pprint import pp


# Player ViewSet
class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


# PlayerStats ViewSet
class PlayerStatsViewSet(viewsets.ModelViewSet):
    queryset = PlayerStats.objects.all()
    serializer_class = PlayerStatsSerializer


# MMRHistory ViewSet
class MMRHistoryViewSet(viewsets.ModelViewSet):
    queryset = MMRHistory.objects.all()
    serializer_class = MMRHistorySerializer


# CharacterStats ViewSet
class CharacterStatsViewSet(viewsets.ModelViewSet):
    queryset = CharacterStats.objects.all()
    serializer_class = CharacterStatsSerializer


########################################
# 전적 검색 Page 필요한 데이터 구성 FBV
########################################

@api_view(['GET'])
@permission_classes([AllowAny])
def register_player(request, nickname):
    if not nickname:
        return Response({"error": "Nickname parameter is required."}, status=status.HTTP_404_NOT_FOUND)
    user_num = ER.get_user_num(nickname=nickname)
    try:
        player, is_created = Player.objects.get_or_create(nickname=nickname, user_num=user_num)
        player_serializer = PlayerSerializer(player)

        player_stats, is_created = update_or_create_player_stats(player)
        player_stats_serializer = PlayerStatsSerializer(player_stats)
        return Response(player_stats_serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


def update_or_create_player_stats(player: Player, season_id: int = CURRENT_SEASON):
    er_user_stats = ER.fetch_user_stats(user_num=player.user_num, season_id=season_id)
    for er_user_stat in er_user_stats:
        # 전적 데이터 검색
        return PlayerStats.objects.update_or_create(
            player=player,
            season_id=season_id,
            matching_mode=er_user_stat.get('matchingMode'),
            matching_team_mode=er_user_stat.get('matchingTeamMode'),
            defaults={
                'mmr': er_user_stat.get('mmr'),
                'rank': er_user_stat.get('rank'),
                'rank_size': er_user_stat.get('rankSize'),
                'rank_percent': er_user_stat.get('rankPercent'),
                'total_games': er_user_stat.get('totalGames'),
                'total_wins': er_user_stat.get('totalWins'),
                'average_rank': er_user_stat.get('averageRank'),
                'total_team_kills': er_user_stat.get('totalTeamKills'),
                'average_kills': er_user_stat.get('averageKills'),
                'average_assistants': er_user_stat.get('averageAssistants'),
                'average_damage': round(BattleRecord.objects.filter(game__user_num__exact=player.user_num,
                                                                    game__season_id__exact=season_id
                                                                    ).aggregate(Avg('damage_to_player')
                                                                                ).get('damage_to_player__avg')),
                'average_hunts': er_user_stat.get('averageHunts'),
                'top1': er_user_stat.get('top1'),
                'top2': er_user_stat.get('top2'),
                'top3': er_user_stat.get('top3'),
                'top5': er_user_stat.get('top5'),
                'top7': er_user_stat.get('top7'),
            }
        )

    pass
