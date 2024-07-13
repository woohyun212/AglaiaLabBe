import requests
from typing import Optional, List, Dict, Any


class BserAPI:
    BASE_URL = 'https://open-api.bser.io'

    def __init__(self, key):
        self.headers = {'x-api-key': key}

    def request_bser(self, urn: str, version: str = 'v1', params: Optional[Dict[str, Any]] = None) -> Dict:
        url = f"{self.BASE_URL}/{version}/{urn}"
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"Other error occurred: {err}")
        return {}

    # data
    # # Fetch game data by metaType
    def fetch_data_by_meta_type(self, meta_type: str) -> Dict:
        """
        :param meta_type: Meta Type, use 'hash' to find all types
        :return:
        """
        return self.request_bser(urn=f'data/{meta_type}')

    # Fetch game data by metaType version2
    def fetch_data_by_meta_type_v2(self, meta_type: str) -> Dict:
        """
        :param meta_type: Meta Type, use 'hash' to find all types
        :return:
        """
        return self.request_bser(urn=f'data/{meta_type}', version='v2')

    # # Fetch freeCharacters by matchingMode
    def fetch_free_characters(self, matching_mode: int) -> Dict:
        """"
        :param matching_mode: matchingMode (2: Normal, 3: Rank)
        """
        return self.request_bser(urn=f'freeCharacters/{matching_mode}')

    # # Fetch l10n data by language
    def fetch_l10n_data(self, language: str) -> Dict:
        """
        :param language: Korean, English, Japanese, ChineseSimplified, ChineseTraditional, French, Spanish,
        SpanishLatin, Portuguese, PortugueseLatin, Indonesian, German, Russian, Thai, Vietnamese
        """
        return self.request_bser(urn=f'l10n/{language}')

    # games
    # # Fetch user games by gameId
    def fetch_games(self, game_id: str, _next: int = 0) -> Dict:
        """
        :param game_id: game id
        :param _next: paging parameter 'next' from previous response
        """
        return self.request_bser(urn=f'games/{game_id}', params={'next': _next})

    # rank/top
    # # Fetch rankders by seasonId, matchingTeamMode
    def fetch_rankers(self, season_id: int, matching_team_mode: int) -> Dict:
        """
        :param season_id: matching Team Mode (1,2,3)
        :param matching_team_mode: season id (for ranking league) / 0 (for normal league)
        """
        return self.request_bser(urn=f'rankers/{season_id}/{matching_team_mode}')

    # rank/user
    # # Fetch user rank by seasonId, matchingTeamMode
    def fetch_leaders(self, user_num: int, season_id: int, matching_team_mode: int) -> Dict:
        """
        :param user_num: user number
        :param season_id: season id (for ranking league) / 0 (for normal league)
        :param matching_team_mode: matching Team Mode (1,2,3)
        """
        return self.request_bser(urn=f'leaders/{user_num}/{season_id}/{matching_team_mode}')

    # user/games
    # # Fetch games by userNum
    def fetch_user_games(self, user_num: int, _next=None) -> Dict:
        """
        :param user_num: user number
        :param _next: paging parameter 'next' from previous response
        """
        if _next:
            return self.request_bser(urn=f'user/games/{user_num}', params={'next': _next})
        return self.request_bser(urn=f'user/games/{user_num}')

    # fetch user by nickname
    # # Fetch user by nickname
    def fetch_user_nickname(self, nickname: str) -> Dict:
        """
        :param nickname: user's nickname
        """
        return self.request_bser(urn='user/nickname', params={'query': nickname})

    def get_user_num(self, nickname: str) -> Optional[int]:
        """
        :param nickname: user's nickname
        유저의 유저 번호를 가져옵니다
        """
        response = self.fetch_user_nickname(nickname)
        if response.get('code') == 200:
            return response.get('user', {}).get('userNum')
        else:
            print(f"Error fetching user number: {response.get('message')}")
            return None

    # user/stats
    # # Fetch stats by userNum and seasonId
    def fetch_user_stats(self, user_num: int, season_id: int) -> Dict:
        """
        :param user_num: user number
        :param season_id: season id (for ranking league) / 0 (for normal league)
        """
        response = self.request_bser(urn=f'user/stats/{user_num}/{season_id}')
        if response.get('code') == 200:
            return response.get('userStats')

    # weaponRoutes/recommend
    # # Fetch recommend weaponRoutes
    def fetch_recommend_weapon_routes(self, _next: str = '') -> List[Dict]:
        response = self.request_bser(urn='weaponRoutes/recommend', params={'next': _next})
        if response.get('code') == 200:
            return response.get('result', [])
        else:
            print(f"Error fetching recommended weapon routes: {response.get('message')}")
            return []

    # # Fetch recommend weaponRoute by route id
    def fetch_recommend_weapon_route(self, route_id: str) -> Dict:
        response = self.request_bser(urn=f'weaponRoutes/recommend/{route_id}')
        if response.get('code') == 200:
            return response.get('result', {})
        else:
            print(f"Error fetching recommended weapon route: {response.get('message')}")
            return {}
