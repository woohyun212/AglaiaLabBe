# Create your models here.
from django.db import models


# 플레이어 정보 모델
class Player(models.Model):
    user_num = models.IntegerField()  # Unique number identifier of the user.
    nickname = models.CharField(max_length=100)  # 이름


# 플레이어 통계 모델
class PlayerStats(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE)
    season_id = models.IntegerField()
    matching_mode = models.IntegerField()  # 2 : Normal, 3 : Ranked
    matching_team_mode = models.IntegerField()  # 1 : Solo,2 : Duo, 3 : Squad

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
    average_damage = models.FloatField()  # 평균 데미지
    average_hunts = models.FloatField()  # 야생 동물 사냥 횟수 평균

    top1 = models.FloatField()  # 1등 비율
    top2 = models.FloatField()  # 2등 비율
    top3 = models.FloatField()  # 3등 비율
    top5 = models.FloatField()  # 5등 비율
    top7 = models.FloatField()  # 7등 비율

    class Meta:
        indexes = [
            models.Index(fields=['player', 'season_id']),
        ]
class MMRHistory(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    open_mmr = models.FloatField()
    high_mmr = models.FloatField()
    low_mmr = models.FloatField()
    close_mmr = models.FloatField()
    timestamp = models.DateTimeField()


class CharacterStats(models.Model):
    player_stats = models.ForeignKey(PlayerStats, on_delete=models.CASCADE)
    character_code = models.IntegerField()

    most_used_skin_code = models.IntegerField()
    most_weapon = models.IntegerField()
    most_tactical_skill_group = models.IntegerField()
    most_trait_first_core = models.IntegerField()
    most_trait_first_sub = models.JSONField()
    most_trait_second_sub = models.JSONField()

    total_games = models.IntegerField()
    average_team_kills = models.FloatField()
    average_kills = models.FloatField()
    average_assistants = models.FloatField()
    average_damage = models.FloatField()
    average_rank = models.FloatField()
    top1 = models.FloatField()
    top2 = models.FloatField()
    top3 = models.FloatField()
    earned_rp = models.IntegerField()
