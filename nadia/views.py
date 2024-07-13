from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views import View

from django.http import JsonResponse
from django.views import View


# URL: /api/home/
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


# URL: /api/player-stats/<player_id>/
# Method: GET
# Description: 특정 플레이어의 통계 시각화
# Response: 플레이어 통계 데이터 (JSON)
class PlayerStatsView(View):
    def get(self, request, player_id):
        # 플레이어 통계 데이터 로직
        data = {
            "player_id": player_id,
            "stats": {
                # 통계 데이터
            }
        }
        return JsonResponse(data)


# URL: /api/leaderboard/
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


# URL: /api/match-history/<player_id>/
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


# URL: /api/character-builds/
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


# URL: /api/events-news/
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


# URL: /api/community/
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

