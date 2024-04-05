import pandas as pd
import json

class Cleaner:
  
  def __init__(self) -> None:
    pass
  
  def initialize(self, files: list[str]) -> pd.DataFrame:
    teams_data = self.extract_teams(files)
    return pd.DataFrame(teams_data)
  
  def extract_teams(self, files: list[str]) -> list[dict]:
    teams_data = []
    for file in files:
      with open(file) as f:
        self.df = json.load(f)
                
        # Vérification pour éviter les doublons
        if self.df['Home']['id'] not in [team['idteam'] for team in teams_data]:
          teams_data.append({'idteam': self.df['Home']['id'], 'name': self.df['Home']['club']})
                    
        if self.df['Away']['id'] not in [team['idteam'] for team in teams_data]:
          teams_data.append({'idteam': self.df['Away']['id'], 'name': self.df['Away']['club']})

    return teams_data
