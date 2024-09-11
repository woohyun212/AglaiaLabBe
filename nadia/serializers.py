from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Player, PlayerStat, MMRHistory, CharacterStats


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


# Player 모델의 Serializer
class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'
        # fields = ['user_num', 'nickname']  # 필요한 필드만 직렬화


# MMRHistory 모델의 Serializer
class MMRHistorySerializer(serializers.ModelSerializer):
    # player = PlayerSerializer()  # Nested serializer to include player info

    class Meta:
        model = MMRHistory
        # fields = '__all__'
        fields = ['open_mmr', 'high_mmr', 'low_mmr', 'close_mmr', 'timestamp']


class FormattedMMRHistorySerializer(serializers.ModelSerializer):
    o = serializers.IntegerField(source='open_mmr')
    h = serializers.IntegerField(source='high_mmr')
    l = serializers.IntegerField(source='low_mmr')
    c = serializers.IntegerField(source='close_mmr')
    x = serializers.DateField(source='timestamp')

    class Meta:
        model = MMRHistory
        fields = ['o', 'h', 'l', 'c', 'x']

    # CharacterStats 모델의 Serializer


class CharacterStatsSerializer(serializers.ModelSerializer):
    # player_stats = PlayerStatsSerializer()  # Nested serializer to include player stats

    class Meta:
        model = CharacterStats
        fields = '__all__'
        # fields = [
        #     'player_stats', 'character_code', 'most_used_skin_code',
        #     'most_weapon', 'most_tactical_skill_group', 'most_trait_first_core',
        #     'most_trait_first_sub', 'most_trait_second_sub', 'total_games',
        #     'average_team_kills', 'average_kills', 'average_assistants',
        #     'average_damage', 'average_rank', 'top1', 'top2', 'top3', 'earned_rp'
        # ]


class PlayerStatsSerializer(serializers.ModelSerializer):
    player = PlayerSerializer()  # Nested serializer to include player info
    average_team_kills = serializers.SerializerMethodField()
    mmr_history = FormattedMMRHistorySerializer(many=True)

    def get_average_team_kills(self, obj):
        # a/b 계산 수행 (b가 0이 아닌 경우만)
        return round(obj.total_team_kills / obj.total_games, 2)

    class Meta:
        model = PlayerStat
        # fields = '__all__'
        fields = [
            'player', 'season_id', 'matching_mode', 'matching_team_mode',
            'mmr', 'rank', 'rank_size', 'rank_percent', 'total_games',
            'total_wins', 'average_rank', 'total_team_kills', 'average_team_kills',
            'average_kills', 'average_assistants', 'average_damage',
            'average_hunts', 'top1', 'top2', 'top3', 'top5', 'top7',
            'mmr_history'
        ]
