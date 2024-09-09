from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from bser_api import BserAPI
from AglaiaLabBE.settings.base import ER_API_KEY

from .models import GameInfo, BattleRecord, EquipmentAndTraits
from .serializers import GameInfoSerializer, GameInfoSimpleSerializer

# BserAPI Instance
ER = BserAPI(ER_API_KEY)
CURRENT_SEASON = 25


class GameInfoViewSet(viewsets.ModelViewSet):
    queryset = GameInfo.objects.all()
    serializer_class = GameInfoSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def get_game_info(request, nickname):
    # 닉네임으로 게임 전적 조회
    games = GameInfo.objects.filter(nickname=nickname)

    if not games.exists():
        return Response({"error": "No game records found for this nickname."}, status=404)

    # 전적 정보를 직렬화하여 반환
    serializer = GameInfoSimpleSerializer(games, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])  # 인증된 사용자만 접근 가능
def fetch_and_add(request, nickname):
    if not nickname:
        return Response({"error": "Nickname parameter is required."}, status=status.HTTP_404_NOT_FOUND)

    # 외부 API 호출 (예시 URL)
    # 외부 API에서 받은 데이터
    api_data = ER.fetch_user_games(ER.get_user_num(nickname=nickname))
    user_stats = api_data.get('userGames', [])

    if not user_stats:
        return Response({"error": "No data found for the given nickname."}, status=status.HTTP_404_NOT_FOUND)

    # # 첫 번째 통계 데이터만 사용 (필요에 따라 여러 개의 통계를 처리할 수 있음)
    # stats = user_stats
    # return Response(stats, status=status.HTTP_200_OK)
    try:
        created_game_infos = []
        for stats in user_stats:
            # GameInfo 저장
            game_info, is_created = GameInfo.objects.get_or_create(
                game_id=stats['gameId'],
                user_num=stats['userNum'],
                defaults={
                    "nickname": stats.get('nickname'),
                    'game_id': stats.get('gameId'),
                    'season_id': stats.get('seasonId'),
                    'matching_mode': stats.get('matchingMode'),
                    'matching_team_mode': stats.get('matchingTeamMode'),
                    'server_name': stats.get('serverName'),
                    'character_num': stats.get('characterNum'),
                    'start_dtm': stats.get('startDtm'),
                    'play_time': stats.get('playTime'),
                    'watch_time': stats.get('watchTime'),
                    'total_time': stats.get('totalTime'),
                    'bot_added': stats.get('botAdded'),
                    'bot_remain': stats.get('botRemain'),
                    'restricted_area_accelerated': stats.get('restrictedAreaAccelerated'),
                    'safe_areas': stats.get('safeAreas'),
                    'team_number': stats.get('teamNumber'),
                    'pre_made': stats.get('preMade'),
                    'victory': stats.get('victory'),
                    'game_rank': stats.get('gameRank'),
                    'mmr_before': stats.get('mmrBefore', None),
                    'mmr_gain': stats.get('mmrGain', None),
                    'mmr_after': stats.get('mmrAfter', None),
                }
            )
            # BattleRecord 저장

            BattleRecord.objects.get_or_create(
                game=game_info,
                character_level=stats['characterLevel'],
                player_kill=stats['playerKill'],
                player_assistant=stats['playerAssistant'],
                monster_kill=stats['monsterKill'],
                max_hp=stats['maxHp'],
                max_sp=stats['maxSp'],
                attack_power=stats['attackPower'],
                move_speed=stats['moveSpeed'],
                defense=stats['defense'],
                hp_regen=stats['hpRegen'],
                sp_regen=stats['spRegen'],
                attack_speed=stats['attackSpeed'],
                sight_range=stats['sightRange'],
                critical_strike_chance=stats['criticalStrikeChance'],
                critical_strike_damage=stats['criticalStrikeDamage'],
                cool_down_reduction=stats['coolDownReduction'],
                life_steal=stats['lifeSteal'],
                damage_to_player=stats['damageToPlayer'],
                damage_to_monster=stats['damageToMonster'],
                damage_from_player=stats['damageFromPlayer'],
                heal_amount=stats['healAmount'],
                protect_absorb=stats['protectAbsorb'],
                total_double_kill=stats['totalDoubleKill'],
                total_triple_kill=stats['totalTripleKill'],
                total_quadra_kill=stats['totalQuadraKill'],
                total_extra_kill=stats['totalExtraKill'],

                killer_user_num=stats['killerUserNum'],
                killer=stats['killer'],
                kill_detail=stats.get('killDetail', None),
                killer_character=stats.get('killerCharacter', None),
                killer_weapon=stats.get('killerWeapon', None),
                cause_of_death=stats.get('causeOfDeath', None),
                place_of_death=stats.get('placeOfDeath', None),

                killer_user_num2=stats['killerUserNum2'],
                killer2=stats.get('killer2', None),
                kill_detail2=stats.get('killDetail2', None),
                killer_character2=stats.get('killerCharacter2', None),
                killer_weapon2=stats.get('killerWeapon2', None),
                cause_of_death2=stats.get('causeOfDeath2', None),
                place_of_death2=stats.get('placeOfDeath2', None),

                killer_user_num3=stats['killerUserNum3'],
                killer3=stats.get('killer3', None),
                kill_detail3=stats.get('killDetail3', None),
                killer_character3=stats.get('killerCharacter3', None),
                killer_weapon3=stats.get('killerWeapon3', None),
                cause_of_death3=stats.get('causeOfDeath3', None),
                place_of_death3=stats.get('placeOfDeath3', None),
            )

            # EquipmentAndTraits 저장
            EquipmentAndTraits.objects.get_or_create(
                game=game_info,
                skin_code=stats['skinCode'],
                best_weapon=stats['bestWeapon'],
                best_weapon_level=stats['bestWeaponLevel'],
                mastery_level=stats['masteryLevel'],
                equipment=stats['equipment'],
                skill_level_info=stats['skillLevelInfo'],
                skill_order_info=stats['skillOrderInfo'],
                trait_first_core=stats['traitFirstCore'],
                trait_first_sub=stats['traitFirstSub'],
                trait_second_sub=stats['traitSecondSub'],
                tactical_skill_group=stats['tacticalSkillGroup'],
                tactical_skill_level=stats['tacticalSkillLevel'],
            )
            created_game_infos.append(game_info)

        # 저장된 데이터를 시리얼라이저로 반환
        serializer = GameInfoSerializer(created_game_infos, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            "error": f"Error saving data: {str(e)}",
        }, status=500)
