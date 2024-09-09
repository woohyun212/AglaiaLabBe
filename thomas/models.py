from django.db import models


# 게임 정보 테이블
class GameInfo(models.Model):
    user_num = models.BigIntegerField()  # 유저 번호
    nickname = models.CharField(max_length=20)  # 유저 닉네임
    game_id = models.BigIntegerField()  # 게임 ID
    season_id = models.IntegerField()  # 시즌 ID
    matching_mode = models.IntegerField()  # 2: 일반, 3: 랭크
    matching_team_mode = models.IntegerField()  # 1: 솔로, 2: 듀오, 3: 스쿼드
    server_name = models.CharField(max_length=100)  # 배틀 서버 지역 이름
    character_num = models.IntegerField()  # 캐릭터 번호
    start_dtm = models.DateTimeField()  # 게임 시작 시간
    play_time = models.IntegerField()  # 유저 플레이 시간 (초)
    watch_time = models.IntegerField()  # 유저 관전 시간 (초)
    total_time = models.IntegerField()  # 총 시간 (초)
    bot_added = models.IntegerField()  # 게임에 참여한 봇 수
    bot_remain = models.IntegerField()  # 게임 종료 시 남은 봇 수
    restricted_area_accelerated = models.BooleanField()  # 금지 구역 가속 여부
    safe_areas = models.IntegerField()  # 종료 시 남은 안전 구역 수
    team_number = models.IntegerField()  # 팀 번호
    pre_made = models.IntegerField()  # 사전 구성된 팀원 수
    victory = models.BooleanField()  # 승리 여부
    game_rank = models.IntegerField()  # 최종 등수
    mmr_before = models.IntegerField(null=True)  # 이전 mmr
    mmr_gain = models.IntegerField(null=True)  # mmr 변화량
    mmr_after = models.IntegerField(null=True)  # 변경된 mmr

    def __str__(self):
        return f"Game {self.game_id} - Player {self.nickname}"

    class Meta:
        unique_together = ('user_num', 'game_id')
        indexes = [
            models.Index(fields=['user_num']),
            models.Index(fields=['game_id']),
        ]


# 전투 기록 테이블
class BattleRecord(models.Model):
    game = models.ForeignKey(GameInfo, on_delete=models.CASCADE)  # 게임 정보와 연결
    user_num = models.BigIntegerField()  # GameInfo의 user_num을 저장
    character_level = models.IntegerField()  # 캐릭터 레벨
    player_kill = models.IntegerField()  # 킬 수
    player_assistant = models.IntegerField()  # 어시스트 수
    monster_kill = models.IntegerField()  # 몬스터 킬 수
    max_hp = models.IntegerField()  # 최대 체력
    max_sp = models.IntegerField()  # 최대 스태미나
    attack_power = models.IntegerField()  # 공격력
    move_speed = models.FloatField()  # 이동 속도
    defense = models.IntegerField()  # 방어력
    hp_regen = models.FloatField()  # 체력 재생
    sp_regen = models.FloatField()  # 스태미나 재생
    attack_speed = models.FloatField()  # 공격 속도
    sight_range = models.FloatField()  # 시야
    critical_strike_chance = models.FloatField()  # 치명타 확률
    critical_strike_damage = models.FloatField()  # 치명타 피해량
    cool_down_reduction = models.FloatField()  # 쿨다운 감소
    life_steal = models.FloatField()  # 피해 흡혈
    damage_to_player = models.IntegerField()  # 플레이어에게 준 피해
    damage_to_monster = models.IntegerField()  # 몬스터에게 준 피해
    damage_from_player = models.IntegerField()  # 플레이어에게 받은 피해
    heal_amount = models.IntegerField()  # 회복량
    protect_absorb = models.IntegerField()  # 보호막 흡수량
    total_double_kill = models.IntegerField()  # 연속 2킬
    total_triple_kill = models.IntegerField()  # 연속 3킬
    total_quadra_kill = models.IntegerField()  # 연속 4킬
    total_extra_kill = models.IntegerField()  # 연속 5킬 이상

    killer_user_num = models.IntegerField()  # 처형자의 유저 번호
    killer = models.CharField(max_length=100, null=True)  # 처형자 구분
    kill_detail = models.CharField(max_length=100, null=True)  # 처형자 닉네임
    killer_character = models.CharField(max_length=100, null=True)  # 처형자 캐릭터
    killer_weapon = models.CharField(max_length=100, null=True)  # 처형자 무기
    cause_of_death = models.CharField(max_length=100, null=True)  # 사망 원인
    place_of_death = models.IntegerField(null=True)  # 사망 지역

    killer_user_num2 = models.IntegerField()  # 처형자의 유저 번호2
    killer2 = models.CharField(max_length=100, null=True)  # 처형자 구분2
    kill_detail2 = models.CharField(max_length=100, null=True)  # 처형자 닉네임2
    killer_character2 = models.CharField(max_length=100, null=True)  # 처형자 캐릭터2
    killer_weapon2 = models.CharField(max_length=100, null=True)  # 처형자 무기2
    cause_of_death2 = models.CharField(max_length=100, null=True)  # 사망 원인2
    place_of_death2 = models.IntegerField(null=True)  # 사망 지역2

    killer_user_num3 = models.IntegerField()  # 처형자의 유저 번호3
    killer3 = models.CharField(max_length=100, null=True)  # 처형자 구분3
    kill_detail3 = models.CharField(max_length=100, null=True)  # 처형자 닉네임3
    killer_character3 = models.CharField(max_length=100, null=True)  # 처형자 캐릭터3
    killer_weapon3 = models.CharField(max_length=100, null=True)  # 처형자 무기3
    cause_of_death3 = models.CharField(max_length=100, null=True)  # 사망 원인3
    place_of_death3 = models.IntegerField(null=True)  # 사망 지역3

    def save(self, *args, **kwargs):
        # game 필드의 GameInfo 객체에서 user_num 값을 자동으로 가져옴
        self.user_num = self.game.user_num
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Battle record for game {self.game.game_id}"

    class Meta:
        unique_together = ('game', 'user_num')


# 장비 및 특성 정보 테이블
class EquipmentAndTraits(models.Model):
    game = models.ForeignKey(GameInfo, on_delete=models.CASCADE)  # 게임 정보와 연결
    user_num = models.BigIntegerField()  # GameInfo의 user_num을 저장
    skin_code = models.IntegerField()  # 사용한 스킨
    best_weapon = models.IntegerField()  # 가장 높은 무기 숙련도 번호
    best_weapon_level = models.IntegerField()  # 가장 높은 무기 숙련도 레벨
    mastery_level = models.JSONField()  # 숙련도 정보 (JSON)
    equipment = models.JSONField()  # 장비 정보 (JSON)
    skill_level_info = models.JSONField()  # 스킬 레벨 정보 (JSON)
    skill_order_info = models.JSONField()  # 스킬 순서 정보 (JSON)
    trait_first_core = models.IntegerField()  # 주 특성의 핵심 슬롯 번호
    trait_first_sub = models.JSONField()  # 주 특성의 보조 슬롯 번호 (JSON)
    trait_second_sub = models.JSONField()  # 보조 특성의 보조 슬롯 번호 (JSON)
    tactical_skill_group = models.IntegerField()  # 전술 스킬 그룹
    tactical_skill_level = models.IntegerField()  # 전술 스킬 레벨

    def save(self, *args, **kwargs):
        # game 필드의 GameInfo 객체에서 user_num 값을 자동으로 가져옴
        self.user_num = self.game.user_num
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Equipment and Traits for game {self.game.game_id}"

    class Meta:
        unique_together = ('game', 'user_num')
