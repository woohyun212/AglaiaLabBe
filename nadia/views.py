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
from django.db.models import Sum, Avg, Count, QuerySet, Case, When, Max
from django.db.models.functions import TruncDate
from pprint import pp


# Player ViewSet
class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


# PlayerStats ViewSet
class PlayerStatsViewSet(viewsets.ModelViewSet):
    queryset = PlayerStat.objects.all()
    serializer_class = PlayerStatsSerializer
    lookup_field = 'player_id'


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
        # Fetch GameInfo based on PlayerStats.
        games = GameInfo.objects.filter(user_num=player_stat.player.user_num, season_id=player_stat.season_id,
                                        matching_mode=player_stat.matching_mode,
                                        matching_team_mode=player_stat.matching_team_mode)

        mmr_histories = update_or_create_mmr_history(player_stat=player_stat, player_games=games)
        character_stats = update_or_create_character_stats(player_stat=player_stat, player_games=games)

    return Response(player_stats_serializer.data, status=status.HTTP_201_CREATED)
    # except Exception as e:
    #     print(e)
    #     return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


def update_or_create_player_stats(player: Player, season_id: int = CURRENT_SEASON):
    er_user_stats = ER.fetch_user_stats(user_num=player.user_num, season_id=season_id)
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
    return player_stats
    pass


def update_or_create_mmr_history(player_stat: PlayerStat, player_games: QuerySet):
    """
    :param player_stat: player_stat
    :param player_games: Fetch GameInfo(s) based on PlayerStats.
    :return: mmr_histories in 10 days
    """
    # Rank Game Data only
    mmr_histories = []
    try:
        # start_dtm에서 날짜만 추출하고 중복되지 않은 날짜들 중 가장 최신 10개 가져오기
        recent_dates = (player_games
                        .annotate(date=TruncDate('start_dtm'))  # 날짜만 추출
                        .order_by('-date')  # 최신 날짜부터 정렬
                        .distinct()  # 중복 제거
                        .values_list('date', flat=True)[:10]  # 최대 10개 가져오기
                        )

        for timestamp in recent_dates:
            one_day_games = player_games.filter(start_dtm__date=timestamp)
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
def update_or_create_character_stats(player_stat: PlayerStat, player_games: QuerySet):
    most_played_characters = (player_games
                              .values('character_num')  # character_num 별로 그룹화
                              .annotate(total_games=Count('character_num'),  # 플레이 횟수 카운트
                                        average_rank=Avg('game_rank'),
                                        total_mmr_gain=Sum('mmr_gain'),
                                        top1=Sum(Case(  # 승리 횟수 카운트
                                            When(victory=True, then=1),
                                            default=0,
                                        )),
                                        top2=Sum(Case(  # 2등 카운트
                                            When(game_rank=2, then=1),
                                            default=0,
                                        )),
                                        top3=Sum(Case(  # 3등 카운트
                                            When(game_rank=3, then=1),
                                            default=0,
                                        )),
                                        max_killings=Max('battle_record__player_kill'),
                                        average_team_kills=Avg('battle_record__team_kill'),
                                        average_kills=Avg('battle_record__player_kill'),
                                        average_assistants=Avg('battle_record__player_assistant'),
                                        average_damage=Avg('battle_record__damage_to_player'),
                                        )
                              .order_by('-total_games')  # 플레이 횟수 기준으로 내림차순 정렬
                              )

    character_stats = []
    for most_played_character in most_played_characters:
        character_code = most_played_character.get('character_num')
        character_games = player_games.filter(character_num=character_code)
        # 각 컬럼의 값을 쿼리셋으로 가져와서 리스트 형태로 추출
        most_used_skin_code_list = character_games.values_list('equipment_and_traits__skin_code', flat=True)
        most_weapon_list = character_games.values_list('equipment_and_traits__best_weapon', flat=True)
        most_tactical_skill_group_list = player_games.values_list('equipment_and_traits__tactical_skill_group',
                                                                  flat=True)
        most_trait_first_core_list = character_games.values_list('equipment_and_traits__trait_first_core', flat=True)
        most_trait_first_sub_list = character_games.values_list('equipment_and_traits__trait_first_sub', flat=True)
        most_trait_second_sub_list = character_games.values_list('equipment_and_traits__trait_second_sub', flat=True)

        from collections import Counter
        # 최빈값 계산
        most_used_skin_code = Counter(most_used_skin_code_list).most_common(1)[0][0]
        most_weapon = Counter(most_weapon_list).most_common(1)[0][0]
        most_tactical_skill_group = Counter(most_tactical_skill_group_list).most_common(1)[0][0]
        most_trait_first_core = Counter(most_trait_first_core_list).most_common(1)[0][0]

        # JSONField인 경우, 내부 데이터를 파싱한 뒤 계산
        most_trait_first_sub = Counter([tuple(sub) for sub in most_trait_first_sub_list]).most_common(1)[0][0]
        most_trait_second_sub = Counter([tuple(sub) for sub in most_trait_second_sub_list]).most_common(1)[0][0]

        # 하나 하나 할당해도 되는데, character_num를 제거해서 귀찮음을 해결
        most_played_character.pop('character_num')
        stat, is_created = CharacterStats.objects.update_or_create(
            player_stat=player_stat,
            character_code=character_code,
            defaults={
                # 'total_games': most_played_character.get('total_games'),
                # 'max_killings': most_played_character.get('max_killings'),
                # 'average_rank': most_played_character.get(),
                # 'top1': most_played_character.get('top1'),
                # 'top2': most_played_character.get(),
                # 'top3': most_played_character.get(),
                # 'total_mmr_gain': most_played_character.get(''),
                #
                # 'average_team_kills': most_played_character.get('a'),
                # 'average_kills': most_played_character.get(),
                # 'average_assistants': most_played_character.get(),
                # 'average_damage': most_played_character.get(),
                'most_used_skin_code': most_used_skin_code,
                'most_weapon': most_weapon,
                'most_tactical_skill_group': most_tactical_skill_group,
                'most_trait_first_core': most_trait_first_core,
                'most_trait_first_sub': most_trait_first_sub,
                'most_trait_second_sub': most_trait_second_sub,
                **most_played_character,

            }
        )
        character_stats.append(stat)
    return character_stats
