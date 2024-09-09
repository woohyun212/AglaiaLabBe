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
    battle_records = BattleRecordSerializer(source='battlerecord_set', many=True, read_only=True)
    equipment_and_traits = EquipmentAndTraitsSerializer(source='equipmentandtraits_set', many=True, read_only=True)

    class Meta:
        model = GameInfo
        fields = '__all__'
        extra_fields = ['battle_records', 'equipment_and_traits']


class GameInfoSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameInfo
        fields = ['nickname',
                  'game_id',
                  'season_id',
                  'matching_mode',
                  # 'matching_team_mode',
                  'game_rank',
                  'character_num',
                  'start_dtm',
                  'play_time',
                  # 'team_number',
                  'pre_made',
                  'mmr_before',
                  'mmr_gain',
                  'mmr_after'
                  ]
