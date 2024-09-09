from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import GameInfo

class GameInfoAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.game_info_data = {
            'user_num': 1,
            'nickname': 'Player1',
            'game_id': 1001,
            'season_id': 2024,
            'matching_mode': 2,
            'matching_team_mode': 1,
            'server_name': 'NA',
            'character_num': 7,
            'start_dtm': '2024-09-09T12:00:00Z',
            'play_time': 3600,
            'watch_time': 1800,
            'total_time': 5400,
            'bot_added': 3,
            'bot_remain': 1,
            'restricted_area_accelerated': False,
            'safe_areas': 2,
            'team_number': 1,
            'pre_made': 0,
            'victory': False,
            'game_rank': 5
        }
        self.game_info = GameInfo.objects.create(**self.game_info_data)

    def test_get_gameinfo_list(self):
        response = self.client.get(reverse('gameinfo-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['game_id'], self.game_info_data['game_id'])

    def test_get_gameinfo_detail(self):
        url = reverse('gameinfo-detail', kwargs={'pk': self.game_info.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['game_id'], self.game_info_data['game_id'])