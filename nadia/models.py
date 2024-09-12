# Create your models here.
from django.db import models


# 플레이어 정보 모델
class Player(models.Model):
    user_num = models.BigIntegerField(primary_key=True, unique=True)  # Unique number identifier of the user.
    nickname = models.CharField(max_length=100)  # 이름

    def __str__(self):
        return f"{self.nickname} - {self.user_num}"


# 플레이어 통계 모델
class PlayerStat(models.Model):
    # OneToOne이 아닌데?
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    season_id = models.IntegerField()
    matching_mode = models.IntegerField()  # 2 : Normal, 3 : Ranked, 6: Cobalt Protocol
    matching_team_mode = models.IntegerField()  # 1 : Solo,2 : Duo, 3 : Squad, 4: 4Squad (코발트 전용)

    mmr = models.IntegerField()  # 현재 mmr
    rank = models.IntegerField()  # 랭크 등수
    rank_size = models.IntegerField()  # 랭크 참여 전체 인원
    rank_percent = models.FloatField()  # 랭크 상위 %
    # 아래 항목은 시리얼라이저 처리 후 데이터 반환하기 직전에 계산해서 API반환하는게 좋을 것 같음
    # tier_mmr = models.IntegerField()  # 현재 tier에서 mmr

    total_games = models.IntegerField()  # 전체 게임 참여 수
    total_wins = models.IntegerField()  # 전체 게임 승리 수
    average_rank = models.FloatField()  # 평균 등수
    total_team_kills = models.IntegerField()  # 전체 TK
    # average_team_kills = models.FloatField()  # 평균 tk는 전체 TK를 total_games로 나눠서 계산하여 db에 저장하면될 것 같은데
    average_kills = models.FloatField()  # 평균 킬
    average_assistants = models.FloatField()  # 평균 어시스트
    average_damage = models.IntegerField()  # 평균 데미지
    average_hunts = models.FloatField()  # 야생 동물 사냥 횟수 평균

    top1 = models.FloatField()  # 1등 비율
    top2 = models.FloatField()  # 2등 비율
    top3 = models.FloatField()  # 3등 비율
    top5 = models.FloatField()  # 5등 비율
    top7 = models.FloatField()  # 7등 비율

    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.player}/{self.season_id}S - {self.matching_mode}M - {self.matching_team_mode}MTM"

    class Meta:
        indexes = [
            models.Index(fields=['player', 'season_id']),
            models.Index(fields=['player', 'season_id', 'matching_mode', 'matching_team_mode']),
        ]


class MMRHistory(models.Model):
    player_stat = models.ForeignKey(PlayerStat, on_delete=models.CASCADE, related_name='mmr_history')
    open_mmr = models.IntegerField()
    high_mmr = models.IntegerField()
    low_mmr = models.IntegerField()
    close_mmr = models.IntegerField()
    timestamp = models.DateField()

    def __str__(self):
        return f"{self.player_stat} - {self.timestamp}"

    class Meta:
        indexes = [
            models.Index(fields=['player_stat']),
        ]


class CharacterStats(models.Model):
    player_stat = models.ForeignKey(PlayerStat, on_delete=models.CASCADE, related_name='character_stats')
    character_code = models.IntegerField()
    # GameInfo 에서
    total_games = models.IntegerField()
    average_rank = models.FloatField()
    top1 = models.FloatField()
    top2 = models.FloatField()
    top3 = models.FloatField()
    total_mmr_gain = models.IntegerField()

    # BattleRecord
    max_killings = models.IntegerField()
    average_team_kills = models.FloatField()
    average_kills = models.FloatField()
    average_assistants = models.FloatField()
    average_damage = models.IntegerField()

    # Equipment and Trait
    most_used_skin_code = models.IntegerField()
    most_weapon = models.IntegerField()
    most_tactical_skill_group = models.IntegerField()
    most_trait_first_core = models.IntegerField()
    most_trait_first_sub = models.JSONField()
    most_trait_second_sub = models.JSONField()

    class Meta:
        indexes = [
            models.Index(fields=['player_stat', 'character_code']),
        ]
