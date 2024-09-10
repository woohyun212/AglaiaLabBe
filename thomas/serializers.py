from rest_framework import serializers
from .models import GameInfo, BattleRecord, EquipmentAndTraits


class BattleRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BattleRecord
        fields = '__all__'


class EquipmentAndTraitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentAndTraits
        fields = '__all__'


class GameInfoSerializer(serializers.ModelSerializer):
    # BattleRecord, EquipmentAndTraits 중첩
    battle_records = BattleRecordSerializer(read_only=True)
    equipment_and_traits = EquipmentAndTraitsSerializer(read_only=True)

    class Meta:
        model = GameInfo
        fields = '__all__'
        extra_fields = ['battle_records', 'equipment_and_traits']


class BattleRecordSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BattleRecord
        fields = [
            'character_level',
            'team_kill',
            'player_kill',
            'player_assistant',
            'damage_to_player'
        ]


class GameInfoSimpleSerializer(serializers.ModelSerializer):
    battle_record = BattleRecordSimpleSerializer(read_only=True)
    # equipment_and_traits = EquipmentAndTraitsSerializer(read_only=True)

    class Meta:
        model = GameInfo
        fields = [
            'nickname',
            'game_id',
            'season_id',
            'matching_mode',
            'matching_team_mode',
            'pre_made',
            # 'team_number',
            'character_num',
            'game_rank',
            'start_dtm',
            'play_time',
            'mmr_gain',
            'battle_record',
        ]
        # extra_fields = ['battle_record',
        #                 'equipment_and_traits'
                        # ]
