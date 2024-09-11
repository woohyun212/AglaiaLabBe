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
from thomas.models import BattleRecord, GameInfo
from django.db.models import Sum, Avg
from django.db.models.functions import TruncDate
from datetime import timedelta, date
from pprint import pp


# Player ViewSet
class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


# PlayerStats ViewSet
class PlayerStatsViewSet(viewsets.ModelViewSet):
    queryset = PlayerStat.objects.all()
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
    # try:
    player, is_created = Player.objects.get_or_create(nickname=nickname, user_num=user_num)
    player_serializer = PlayerSerializer(player)

    player_stats = update_or_create_player_stats(player)
    player_stats_serializer = PlayerStatsSerializer(player_stats, many=True)

    for player_stat in player_stats:
        mmr_histories = update_or_create_mmr_history(player_stat)

    return Response(player_stats_serializer.data, status=status.HTTP_201_CREATED)
    # except Exception as e:
    #     print(e)
    #     return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


def update_or_create_player_stats(player: Player, season_id: int = CURRENT_SEASON):
    er_user_stats = ER.fetch_user_stats(user_num=player.user_num, season_id=season_id)
    # TODO: Solo, Duo 도 따로 처리 해줘야 함6
    player_stats = []
    for er_user_stat in er_user_stats:
        # 전적 데이터 검색
        average_damage = BattleRecord.objects.filter(game__user_num__exact=player.user_num,
                                                     game__season_id__exact=season_id
                                                     ).aggregate(Avg('damage_to_player')
                                                                 ).get('damage_to_player__avg')
        stat, is_created = PlayerStat.objects.update_or_create(
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
                'average_damage': round(average_damage),
                'average_hunts': er_user_stat.get('averageHunts'),
                'top1': er_user_stat.get('top1'),
                'top2': er_user_stat.get('top2'),
                'top3': er_user_stat.get('top3'),
                'top5': er_user_stat.get('top5'),
                'top7': er_user_stat.get('top7'),
            }
        )
        player_stats.append(stat)

        update_or_create_character_stats(stat, er_character_stats=er_user_stat.get('characterStats', None))

    return player_stats
    pass


def update_or_create_mmr_history(player_stat: PlayerStat):
    # Rank Game Data only
    mmr_histories = []
    try:
        # Fetch GameInfo based on PlayerStats.
        games = GameInfo.objects.filter(user_num=player_stat.player.user_num, season_id=player_stat.season_id,
                                        matching_mode=player_stat.matching_mode,
                                        matching_team_mode=player_stat.matching_team_mode)

        # start_dtm에서 날짜만 추출하고 중복되지 않은 날짜들 중 가장 최신 10개 가져오기
        recent_dates = (games
                        .annotate(date=TruncDate('start_dtm'))  # 날짜만 추출
                        .order_by('-date')  # 최신 날짜부터 정렬
                        .distinct()  # 중복 제거
                        .values_list('date', flat=True)[:10]  # 최대 10개 가져오기
                        )

        for timestamp in recent_dates:
            one_day_games = games.filter(start_dtm__date=timestamp)
            if one_day_games:
                mmr_history, is_created = MMRHistory.objects.update_or_create(
                    player_stat=player_stat,
                    timestamp=timestamp,
                    defaults={
                        'open_mmr': one_day_games.earliest('start_dtm').mmr_before,  # 특정 날짜에서 때 가장 빠른 값.
                        'high_mmr': one_day_games.order_by('-mmr_after').first().mmr_after,  # 특정 날짜에서 mmr이 가장 높은 값.
                        'low_mmr': one_day_games.order_by('mmr_after').first().mmr_after,  # 특정 날짜에서 때 mmr이 가장 낮은 값.
                        'close_mmr': one_day_games.latest('start_dtm').mmr_after,  # 특정 날짜에서 때 가장 늦은 값
                    }
                )
                mmr_histories.append(mmr_history)
    except PlayerStat.DoesNotExist as e:
        print(e)
    return mmr_histories


# TODO: API에서 불러온 값 저장하고 캐릭터 통계 Object Manager 계산해야함
def update_or_create_character_stats(player_stat: PlayerStat, er_character_stats: dict):
    if er_character_stats is None:
        return None

    character_stats = []
    for er_character_stat in er_character_stats:
        pp(er_character_stat)
        stat, is_created = CharacterStats.objects.update_or_create(
            player_stat=player_stat,
            character_stats=er_character_stat.get('characterCode'),
            defaults={
                'total_mmr_gain': 0,  # GameInfo에서 mmr 획득 총량 계산하기
                'maxKillings': er_character_stat.get('maxKillings'),
                'total_games': er_character_stat.get('usages'),
                'total_wins': er_character_stat.get('totalWins'),
                'average_rank': er_character_stat.get('averageRank'),
                # 'total_team_kills': er_character_stat.get('totalTeamKills'),
                # 'average_kills': er_character_stat.get('averageKills'),
                # 'average_assistants': er_character_stat.get('averageAssistants'),
                'average_damage': 0,  # 얘도 평딜 계산 필요
                # 'top1': er_character_stat.get('top1'),
                # 'top2': er_character_stat.get('top2'),
                # 'top3': er_character_stat.get('top3'),
            }
        )
    try:

        pass
    except Exception as e:
        print(e)
