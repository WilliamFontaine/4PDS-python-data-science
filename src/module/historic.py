import pandas as pd

class Historic:
  
  def __init__(self) -> None:
    pass
  
  def compute(self, matchs: pd.DataFrame, match_players: pd.DataFrame, players: pd.DataFrame, teams: pd.DataFrame) -> pd.DataFrame:
    merged_data = pd.merge(matchs, match_players, left_on='idmatch', right_on='matchid', how='inner')
    merged_data = pd.merge(merged_data, players, left_on='playerid', right_on='idplayer', how='inner')
    merged_data = pd.merge(merged_data, teams, left_on='teamid', right_on='idteam', how='inner')
    merged_data = merged_data.drop(columns=['idteam_home', 'idteam_away']).sort_values(by='date')
    
    player_team = pd.DataFrame(columns=['player_id', 'name', 'team', 'starting_date', 'end_date'])
    
    for _, data in merged_data.iterrows():
      player_id = data['playerid']
      player_name = data['lastname']
      team = data['name']
      date = data['date']
      
      last_entry = player_team[player_team['player_id'] == player_id]
      
      if last_entry.empty:
        player_team.loc[len(player_team)] = {
          'player_id': player_id,
          'name': player_name,
          'team': team,
          'starting_date': date,
          'end_date': None
        }
        continue     
             
      last_entry = last_entry.sort_values(by='starting_date').iloc[-1]
      if last_entry['team'] != team:
        player_team.loc[last_entry.name, 'end_date'] = date
        player_team.loc[len(player_team)] = {
          'player_id': player_id,
          'name': player_name,
          'team': team,
          'starting_date': date,
          'end_date': None
        }

    return player_team
    
