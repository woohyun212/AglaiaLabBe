from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class CharacterStatSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CharacterStatModel
        fields = '__all__'
    # averageRank = serializers.FloatField()
    # characterCode = serializers.IntegerField()
    # maxKillings = serializers.IntegerField()
    # top3 = serializers.IntegerField()
    # top3Rate = serializers.FloatField()
    # totalGames = serializers.IntegerField()
    # usages = serializers.IntegerField()
    # wins = serializers.IntegerField()


class PlayerStatsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = PlayerStatsModel
        fields = '__all__'

        # TODO : extra_kwargs 관련 내용 정리 하기
        # 난 pk 가 아닌 nickname 으로 데이터를 불러오려고 했었음
        # pk가 아닌 다른 값을 통해 detail 조회를 하려고하니 아래와 같은 오류가 났었음
        # Could not resolve URL for hyperlinked relationship using view name "playerstatsmodel-detail".
        # You may have failed to include the related model in your API, or incorrectly configured the `lookup_field` attribute on this field.
        # extra_kwargs 속성 추가 후 정상화

        extra_kwargs = {
            'url': {'lookup_field': 'nickname'}
        }

    # userNum = serializers.IntegerField()
    # nickname = serializers.CharField(max_length=100)
    # seasonId = serializers.IntegerField()
    # matchingMode = serializers.IntegerField()
    # matchingTeamMode = serializers.IntegerField()
    # mmr = serializers.IntegerField()
    # rank = serializers.IntegerField()
    # rankPercent = serializers.FloatField()
    # rankSize = serializers.IntegerField()
    # totalGames = serializers.IntegerField()
    # totalWins = serializers.IntegerField()
    # totalTeamKills = serializers.IntegerField()
    # totalDeaths = serializers.IntegerField()
    # escapeCount = serializers.IntegerField()
    # averageRank = serializers.FloatField()
    # averageKills = serializers.FloatField()
    # averageAssistants = serializers.FloatField()
    # averageHunts = serializers.FloatField()
    # top1 = serializers.FloatField()
    # top2 = serializers.FloatField()
    # top3 = serializers.FloatField()
    # top5 = serializers.FloatField()
    # top7 = serializers.FloatField()
    # characterStats = CharacterStatSerializer(many=True)
