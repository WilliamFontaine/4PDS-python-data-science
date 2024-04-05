import pandas as pd
import json

class Cleaner:
  
  def __init__(self) -> None:
    pass
  
  def initialize(self, files: list[str]) -> pd.DataFrame:
    teams_data = []
    players_data = []
    for file in files:
      with open(file) as f:
        data = json.load(f)
        self.init_teams_data(data, teams_data)
        self.init_players_data(data, players_data)
    return pd.DataFrame(teams_data), pd.DataFrame(players_data)
  
#----------------- Team data initialization -----------------#
  
  def init_teams_data(self, data: dict, teams_data: list[dict]) -> None:
    home_id = data['Home']['id']
    away_id = data['Away']['id']
    home_club = data['Home']['club']
    away_club = data['Away']['club']
    
    self.add_team_data(teams_data, home_id, home_club)
    self.add_team_data(teams_data, away_id, away_club)

  def add_team_data(self, teams_data: list[dict], team_id: str, team_name: str) -> None:
    for team in teams_data:
      if team['idteam'] == team_id:
        return
    teams_data.append({'idteam': team_id, 'name': team_name})
    
#----------------- Player data initialization -----------------#
  
  def init_players_data(self, data: dict, players_data: list[dict]) -> None:
    home_players = data['Home']['players']
    away_players = data['Away']['players']
    
    self.add_players_data(players_data, home_players)
    self.add_players_data(players_data, away_players)
  
  def add_players_data(self, players_data: list[dict], players: dict) -> None:
    for player_id, player_data in players.items():
      if not any(player['idplayer'] == player_data['info']['idplayer'] for player in players_data):
        players_data.append({'idplayer': player_data['info']['idplayer'], 'lastname': player_data['info']['lastname']})
