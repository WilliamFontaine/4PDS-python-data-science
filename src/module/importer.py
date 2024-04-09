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
KEY_MATCH_DATA = 'matchData'
KEY_PERIOD = 'period'
KEY_CHAMPIONSHIP = 'championship'
KEY_QUOTATION_PREGAME = 'quotationPreGame'
KEY_QUOTATION_PLAYERS = 'quotationPlayers'
KEY_SCORE = 'score'

class Importer:
  
    def __init__(self) -> None:
        pass
  
    def initialize(self, files: list[str]) -> tuple:
        teams_data = []
        players_data = []
        matchs_data = []
        highlights_data = []
        substitutions_data = []
        match_players_data = []
        
        for file in files:
            with open(file) as f:
                data = json.load(f)
                self.init_teams_data(data, teams_data)
                self.init_players_data(data, players_data)
                self.init_match_data(data, matchs_data)
                self.init_highlights_data(data, highlights_data)
                self.init_substitutions_data(data, substitutions_data)
                self.init_match_players_data(data, match_players_data)
                
        return (pd.DataFrame(teams_data),
                pd.DataFrame(players_data),
                pd.DataFrame(matchs_data),
                pd.DataFrame(highlights_data),
                pd.DataFrame(substitutions_data),
                pd.DataFrame(match_players_data))
      
    # ------------------- init teams data ------------------- #
  
    def init_teams_data(self, data: dict, teams_data: list[dict]) -> None:
        home_id, away_id = data[KEY_HOME][KEY_ID], data[KEY_AWAY][KEY_ID]
        home_club, away_club = data[KEY_HOME][KEY_CLUB], data[KEY_AWAY][KEY_CLUB]
        
        self.add_team_data(teams_data, home_id, home_club)
        self.add_team_data(teams_data, away_id, away_club)

    def add_team_data(self, teams_data: list[dict], team_id: str, team_name: str) -> None:
        if not any(team[KEY_ID_TEAM] == team_id for team in teams_data):
            teams_data.append({KEY_ID_TEAM: team_id, 'name': team_name})
            
    # ------------------- init players data ------------------- #
    
    def init_players_data(self, data: dict, players_data: list[dict]) -> None:
        home_players, away_players = data[KEY_HOME][KEY_PLAYERS], data[KEY_AWAY][KEY_PLAYERS]
        self.add_players_data(players_data, home_players)
        self.add_players_data(players_data, away_players)
  
    def add_players_data(self, players_data: list[dict], players: dict) -> None:
        for _, player_data in players.items():
            if not any(player[KEY_ID_PLAYER] == player_data[KEY_INFO][KEY_ID_PLAYER] for player in players_data):
                players_data.append({KEY_ID_PLAYER: player_data[KEY_INFO][KEY_ID_PLAYER], KEY_LASTNAME: player_data[KEY_INFO][KEY_LASTNAME]})

    # ------------------- init match data ------------------- #

    def init_match_data(self, data: dict, matchs_data: list[dict]) -> None:
        home_players, away_players = data[KEY_HOME][KEY_PLAYERS], data[KEY_AWAY][KEY_PLAYERS]
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

    # ------------------- init highlights data ------------------- #

    def init_highlights_data(self, data: dict, highlights_data: list[dict]) -> None:
        home_team, away_team = data[KEY_MATCH_DATA][KEY_HOME.lower()], data[KEY_MATCH_DATA][KEY_AWAY.lower()]
        
        home_goals, away_goals = home_team['goals'], away_team['goals']
        home_bookings, away_bookings = home_team['bookings'], away_team['bookings']

        self.add_highlights(highlights_data, home_goals + away_goals, data, 'goal')
        self.add_highlights(highlights_data, home_bookings + away_bookings, data, 'booking')

    def add_highlights(self, highlights_data: list[dict], events: list[dict], data: dict, key: str) -> None:
        for event in events:
            highlights_data.append({
                'idmatch': data[KEY_ID],
                'time': event['time'],
                'idplayer': event['playerId'],
                'event': key,
                'type': event['type']
            })
            
    # ------------------- init substitutions data ------------------- #
            
    def init_substitutions_data(self, data: dict, substitutions_data: list[dict]) -> None:
        home_substitutions, away_substitutions = data[KEY_MATCH_DATA][KEY_HOME.lower()]['substitutions'], data[KEY_MATCH_DATA][KEY_AWAY.lower()]['substitutions']
        
        self.add_substitutions(substitutions_data, home_substitutions + away_substitutions, data)

    def add_substitutions(self, substitutions_data: list[dict], substitutions: list[dict], data: dict) -> None:
        for substitution in substitutions:
            substitution_entry = {
                'idmatch': data[KEY_ID],
                'time': substitution['time'],
                'off_playerId': substitution['subOff'],
                'on_playerId': substitution['subOn']
            }
            if 'reason' in substitution:
                substitution_entry['reason'] = substitution['reason']
            substitutions_data.append(substitution_entry)

    # ------------------- init match players data ------------------- #

    def init_match_players_data(self, data: dict, match_players_data: list[dict]) -> None:
        home_players, away_players = data[KEY_HOME][KEY_PLAYERS], data[KEY_AWAY][KEY_PLAYERS]
        
        self.add_match_players(match_players_data, home_players, data)
        self.add_match_players(match_players_data, away_players, data)
        
    def add_match_players(self, match_players_data: list[dict], players: dict, data: dict) -> None:
        for _, player_data in players.items():
            data_entry = {
                'playerid': player_data[KEY_INFO][KEY_ID_PLAYER],
                'matchid': data[KEY_ID],
                'teamid': player_data[KEY_INFO][KEY_ID_TEAM],
                'position': player_data[KEY_INFO]['position'],
                'formation_place': player_data[KEY_INFO]['formation_place'],
                'play_duration': player_data[KEY_INFO]['mins_played']
            }
        
            if 'note_final_2015' in player_data[KEY_INFO]:
                data_entry['final_mark_2015'] = player_data[KEY_INFO]['note_final_2015']

            if KEY_QUOTATION_PLAYERS in data and data[KEY_QUOTATION_PLAYERS] and f"player_{player_data[KEY_INFO][KEY_ID_PLAYER]}" in data[KEY_QUOTATION_PLAYERS]:
                data_entry['quotation_player'] = data[KEY_QUOTATION_PLAYERS][f"player_{player_data[KEY_INFO][KEY_ID_PLAYER]}"]
                
            for key, value in player_data['stat'].items():
                if key != KEY_INFO:
                    data_entry[key] = value
                
            match_players_data.append(data_entry)

