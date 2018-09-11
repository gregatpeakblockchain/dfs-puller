import requests
import json
import pandas as pd
from pandas.io.json import json_normalize

main_df = pd.DataFrame()

for position in ['qb', 'rb', 'wr', 'te', 'defense', 'kicker']:
    r = requests.get("https://d1qacz8ndd7avl.cloudfront.net/lineuphq/v1.00/2018-09-11/1/base/nfl-{}.json?timestamp=1536688800000".format(position)).json()

    # First Name, # Last Name, #Position, # Team, # Salary, # Projected, # Floor, # Ceiling
    # Site id 2 - Fan Duel
    # Site id 20 - Draft Kings 

    for player_id, player_dict  in r['data']['results'].items():
        data = {}
        data['first_name'] = player_dict['player']['first_name']
        data['last_name'] = player_dict['player']['last_name']
        data['position'] = player_dict['player']['position']
        #data['floor'] = player_dict['floor']
        #data['ceiling'] = player_dict['ceiling']
        data['next_game'] = player_dict['schedule']['date']
        data['projected'] = player_dict['fpts']['2']
        data['o_u'] = player_dict['vegas']['o/u']
        data['total_score'] = player_dict['vegas']['total']
        team_id = player_dict['player']['team_id']
        if player_dict['schedule']['team_home']['id'] == team_id:
            data['team'] = player_dict['schedule']['team_home']['hashtag']
            data['opp'] = player_dict['schedule']['team_away']['hashtag']
        else:
            data['team'] = player_dict['schedule']['team_away']['hashtag']
            data['opp'] = player_dict['schedule']['team_home']['hashtag']
        for salary in player_dict['schedule']['salaries']:
            if salary['site_id'] == 2:
                data['salary_fd'] = salary['salary']
            elif salary['site_id'] == 20:
                data['salary_dk'] = salary['salary']
        df = json_normalize(data)
        main_df = main_df.append(df, ignore_index=True)

main_df.to_csv("players.csv", index=False, columns=['first_name', 'last_name', 'position', 'team', 'next_game', 'opp', 'o_u', 'total_score', 'salary_dk', 'salary_fd', 'projected'], na_rep="NA")
