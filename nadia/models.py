from django.db import models


# Create your models here.
class PlayerStatsModel(models.Model):
    user_num = models.IntegerField()
    nickname = models.CharField(max_length=100)
    season_id = models.IntegerField()
    matching_mode = models.IntegerField(choices=[(2, 'Normal'), (3, 'Ranked')])
    matching_team_mode = models.IntegerField(choices=[(1, 'Solo'), (2, 'Duo'), (3, 'Squad')])
    mmr = models.IntegerField()
    rank = models.IntegerField()
    rank_percent = models.FloatField()
    rank_size = models.IntegerField()
    total_games = models.IntegerField()
    total_wins = models.IntegerField()
    total_team_kills = models.IntegerField()
    total_deaths = models.IntegerField()
    escape_count = models.IntegerField()
    average_rank = models.FloatField()
    average_kills = models.FloatField()
    average_assistants = models.FloatField()
    average_hunts = models.FloatField()
    top1 = models.FloatField()
    top2 = models.FloatField()
    top3 = models.FloatField()
    top5 = models.FloatField()
    top7 = models.FloatField()

    def __str__(self):
        return self.nickname


class CharacterStatModel(models.Model):
    player_stats = models.ForeignKey(PlayerStatsModel, related_name='character_stats', on_delete=models.CASCADE)
    season_id = models.IntegerField()
    average_rank = models.FloatField()
    character_code = models.IntegerField()
    max_killings = models.IntegerField()
    top3 = models.IntegerField()
    top3_rate = models.FloatField()
    total_games = models.IntegerField()
    usages = models.IntegerField()
    wins = models.IntegerField()

    def __str__(self):
        return f"Character {self.character_code} Stats"
