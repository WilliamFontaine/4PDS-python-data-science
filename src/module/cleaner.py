import pandas as pd
import json

KEY_ID = 'id'
KEY_ID_PLAYER = 'idplayer'
KEY_ID_TEAM = 'idteam'
KEY_ID_MATCH = 'idmatch'

KEY_HOME = 'Home'
KEY_AWAY = 'Away'
KEY_DRAW = 'Draw'
KEY_CLUB = 'club'
KEY_PLAYERS = 'players'
KEY_LASTNAME = 'lastname'
KEY_INFO = 'info'
KEY_FORMATION_USED = 'formation_used'
KEY_DATE_MATCH = 'dateMatch'
KEY_MATCH_TIME = 'matchTime'
KEY_PERIOD = 'period'
KEY_CHAMPIONSHIP = 'championship'
KEY_QUOTATION_PREGAME = 'quotationPreGame'
KEY_SCORE = 'score'

class Cleaner:
  
    def __init__(self) -> None:
        pass
  
    def initialize(self, files: list[str]) -> pd.DataFrame:
        teams_data = []
        players_data = []
        matchs_data = []
        for file in files:
            with open(file) as f:
                data = json.load(f)
                self.init_teams_data(data, teams_data)
                self.init_players_data(data, players_data)
                self.init_match_data(data, matchs_data)
        return pd.DataFrame(teams_data), pd.DataFrame(players_data), pd.DataFrame(matchs_data)
      
      
# ------------------- init teams data ------------------- #
  
    def init_teams_data(self, data: dict, teams_data: list[dict]) -> None:
        home_id = data[KEY_HOME][KEY_ID]
        away_id = data[KEY_AWAY][KEY_ID]
        home_club = data[KEY_HOME][KEY_CLUB]
        away_club = data[KEY_AWAY][KEY_CLUB]
    
        self.add_team_data(teams_data, home_id, home_club)
        self.add_team_data(teams_data, away_id, away_club)

    def add_team_data(self, teams_data: list[dict], team_id: str, team_name: str) -> None:
        if not any(team[KEY_ID_TEAM] == team_id for team in teams_data):
            teams_data.append({KEY_ID_TEAM: team_id, 'name': team_name})
            
# ------------------- init players data ------------------- #
    
    def init_players_data(self, data: dict, players_data: list[dict]) -> None:
        home_players = data[KEY_HOME][KEY_PLAYERS]
        away_players = data[KEY_AWAY][KEY_PLAYERS]
    
        self.add_players_data(players_data, home_players)
        self.add_players_data(players_data, away_players)
  
    def add_players_data(self, players_data: list[dict], players: dict) -> None:
        for player_id, player_data in players.items():
            if not any(player[KEY_ID_PLAYER] == player_data[KEY_INFO][KEY_ID_PLAYER] for player in players_data):
                players_data.append({KEY_ID_PLAYER: player_data[KEY_INFO][KEY_ID_PLAYER], KEY_LASTNAME: player_data[KEY_INFO][KEY_LASTNAME]})

# ------------------- init match data ------------------- #

    def init_match_data(self, data: dict, matchs_data: list[dict]) -> None:
        home_players = data[KEY_HOME][KEY_PLAYERS]
        away_players = data[KEY_AWAY][KEY_PLAYERS]
        
        championship = data.get(KEY_CHAMPIONSHIP)
        quotation_pre_game = data.get(KEY_QUOTATION_PREGAME, {})
          
        home_formation_data = self.extract_formation_data(home_players)
        away_formation_data = self.extract_formation_data(away_players)
      
        match_data = {
            'idmatch': data[KEY_ID],
            'date': data[KEY_DATE_MATCH],
            'idteam_home': data[KEY_HOME][KEY_ID], 
            'idteam_away': data[KEY_AWAY][KEY_ID],
            'duration': data[KEY_MATCH_TIME],
            'period': data[KEY_PERIOD],
            'championship': championship,
            'home_formation': home_formation_data,
            'away_formation': away_formation_data,
            'quotation_home': quotation_pre_game.get(KEY_HOME),
            'quotation_away': quotation_pre_game.get(KEY_AWAY),
            'quotation_draw': quotation_pre_game.get(KEY_DRAW),
            'home_score': data[KEY_HOME][KEY_SCORE],
            'away_score': data[KEY_AWAY][KEY_SCORE]
        }
      
        matchs_data.append(match_data)
      
    def extract_formation_data(self, formation: dict) -> str:
        for _, player_data in formation.items():
            return player_data[KEY_INFO][KEY_FORMATION_USED]
