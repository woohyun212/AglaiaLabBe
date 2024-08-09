from django.contrib.admin.utils import lookup_field
from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views import View


# URL: /api/v1/home/
# Method: GET
# Description: 주요 기능 소개 및 접근 경로 제공
# Response: 주요 기능 소개 데이터 (JSON)
class HomePageView(View):
    def get(self, request):
        data = {
            "features": [
                "전적 분석",
                "리더보드",
                "매치 히스토리",
                "캐릭터 빌드 가이드",
                "이벤트 및 뉴스",
                "커뮤니티"
            ]
        }
        return JsonResponse(data)





# URL: /api/v1/leaderboard/
# Method: GET
# Description: 전 세계 또는 지역별 플레이어 순위 제공
# Response: 리더보드 데이터 (JSON)
class LeaderboardView(View):
    def get(self, request):
        # 리더보드 데이터 로직
        data = {
            "leaderboard": [
                # 플레이어 순위 데이터
            ]
        }
        return JsonResponse(data)


# URL: /api/v1/match-history/<player_id>/
# Method: GET
# Description: 특정 플레이어의 게임 기록 제공
# Response: 매치 히스토리 데이터 (JSON)
class MatchHistoryView(View):
    def get(self, request, player_id):
        # 매치 히스토리 데이터 로직
        data = {
            "player_id": player_id,
            "matches": [
                # 매치 데이터
            ]
        }
        return JsonResponse(data)


# URL: /api/v1/character-builds/
# Method: GET
# Description: 캐릭터별 빌드와 전략 제공
# Response: 캐릭터 빌드 데이터 (JSON)
class CharacterBuildsView(View):
    def get(self, request):
        # 캐릭터 빌드 데이터 로직
        data = {
            "builds": [
                # 캐릭터 빌드 데이터
            ]
        }
        return JsonResponse(data)


# URL: /api/v1/events-news/
# Method: GET
# Description: 최신 이벤트 및 업데이트 소식 제공
# Response: 이벤트 및 뉴스 데이터 (JSON)
class EventsNewsView(View):
    def get(self, request):
        # 이벤트 및 뉴스 데이터 로직
        data = {
            "events": [
                # 이벤트 데이터
            ],
            "news": [
                # 뉴스 데이터
            ]
        }
        return JsonResponse(data)


# URL: /api/v1/community/
# Method: GET
# Description: 포럼 및 게시판 기능 제공
# Response: 커뮤니티 게시글 데이터 (JSON)
class CommunityView(View):
    def get(self, request):
        # 커뮤니티 게시글 데이터 로직
        data = {
            "posts": [
                # 커뮤니티 게시글 데이터
            ]
        }
        return JsonResponse(data)


######################################
from rest_framework import viewsets
from .serializers import *


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


######################################
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import PlayerStatsSerializer

import requests
from bser_api import BserAPI
from AglaiaLabBE.settings.base import ER_API_KEY

# BserAPI Instance
er_api = BserAPI(ER_API_KEY)
CURRENT_SEASON = 25


# URL: /api/v1/player-stats/<player_name>/
# Method: GET
# Description: 특정 플레이어의 통계 시각화
# Response: 플레이어 통계 데이터 (JSON)
class PlayerStatsViewSet(viewsets.ModelViewSet):
    serializer_class = PlayerStatsSerializer
    queryset = PlayerStatsModel.objects.all()
    lookup_field = 'nickname'
    def retrieve(self, request, nickname):
        season = request.query_params.get('season', CURRENT_SEASON)

        # 외부 API 호출하여 데이터 가져오기
        try:
            user_num = er_api.get_user_num(nickname)
            user_stat = er_api.fetch_user_stats(user_num=user_num, season_id=season)
            data = user_stat[0]

            # PlayerStatsModel에 해당 데이터 저장
            player_stats, created = PlayerStatsModel.objects.update_or_create(
                user_num=user_num,
                defaults={
                    'nickname': nickname,
                    'season_id': season,
                    'matching_mode': data['matchingMode'],
                    'matching_team_mode': data['matchingTeamMode'],
                    'mmr': data['mmr'],
                    'rank': data['rank'],
                    'rank_percent': data['rankPercent'],
                    'rank_size': data['rankSize'],
                    'total_games': data['totalGames'],
                    'total_wins': data['totalWins'],
                    'total_team_kills': data['totalTeamKills'],
                    'total_deaths': data['totalDeaths'],
                    'escape_count': data['escapeCount'],
                    'average_rank': data['averageRank'],
                    'average_kills': data['averageKills'],
                    'average_assistants': data['averageAssistants'],
                    'average_hunts': data['averageHunts'],
                    'top1': data['top1'],
                    'top2': data['top2'],
                    'top3': data['top3'],
                    'top5': data['top5'],
                    'top7': data['top7'],
                }
            )

            # CharacterStatModel에 캐릭터 통계 저장
            for character_stat in data['characterStats']:
                CharacterStatModel.objects.update_or_create(
                    player_stats=player_stats,
                    character_code=character_stat['characterCode'],
                    defaults={
                        'average_rank': character_stat['averageRank'],
                        'max_killings': character_stat['maxKillings'],
                        'top3': character_stat['top3'],
                        'top3_rate': character_stat['top3Rate'],
                        'total_games': character_stat['totalGames'],
                        'usages': character_stat['usages'],
                        'wins': character_stat['wins'],
                    }
                )

            # 저장된 데이터를 직렬화하여 반환
            serializer = PlayerStatsSerializer(player_stats, context={'request': request})
            return Response(serializer.data)

        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)