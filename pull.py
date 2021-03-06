import requests
import json
import pandas as pd
from pandas.io.json import json_normalize
import nflgame
from pydfs_lineup_optimizer import Player
from pydfs_lineup_optimizer import get_optimizer, Site, Sport

print ("[*] Loading Data.")
main_df = pd.DataFrame()
last_df = pd.read_csv("test.csv")
last_df.fillna(0)

def base_fantasy_points(player):
    """
    Baseline points consist of only passing, rushing, receiving, and extra
    point stat categories.

    All punt returns, kick returns, and field goals are calculated later by
    evaluating all plays and are generated separately.
    """
    points = +0.04*getattr(player, 'passing_yds')
    if getattr(player, 'passing_yds') >= 300:
        points += 3
    points += +4*getattr(player, 'passing_tds')
    points += -1*getattr(player, 'passing_ints')
    points += +0.1*getattr(player, 'rushing_yds')
    if getattr(player, 'rushing_yds') >= 100:
        points += 3
    points += +6*getattr(player, 'rushing_tds')
    points += +1*getattr(player, 'receiving_rec')
    points += +0.1*getattr(player, 'receiving_yds')
    if getattr(player, 'receiving_yds') >= 100:
        points += 3
    points += +6*getattr(player, 'receiving_tds')
    points += -1*getattr(player, 'fumbles_lost')
    points += +2*getattr(player, 'passing_twoptm')
    points += +2*getattr(player, 'rushing_twoptm')
    points += +2*getattr(player, 'receiving_twoptm')
    return points

games = nflgame.games(2018, week=1)
players = nflgame.combine_max_stats(games)
optimizer = get_optimizer(Site.DRAFTKINGS, Sport.FOOTBALL)
player_list = []
print ("[*] Downloading projection data.")
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
        if data['position'] == "D":
            data['position'] = "DST"
        elif data['position'] == "WR" or data['position'] == "RB" or data['position'] == "TE":
            data['position'] = "{}/FLEX".format(data['position'])
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
                data['salary_fd'] = float(salary['salary'])
            elif salary['site_id'] == 20:
                data['salary_dk'] = float(salary['salary'])

        for player in players:
            if player.player:
                if player.player.name == "{} {}".format(data['first_name'], data['last_name']):
                    pts = base_fantasy_points(player)
                    data['last_pts'] = pts
        try:
            data['last_proj'] = last_df[last_df.Name == "{} {}".format(data['first_name'], data['last_name'])].Projected.values[0]
        except:
            data['last_proj'] = 0
        df = json_normalize(data)
        main_df = main_df.append(df, ignore_index=True, sort=False)
        try:
            player_list.append(Player(int(player_dict['id']), str(data['first_name']), str(data['last_name']), data['position'].split("/"), data['team'], data['salary_dk'], float(data['projected'])))
        except Exception as e:
            continue

print ("[*] Calculating percent change from last week.")
main_df['pct_change'] = (main_df.last_pts - main_df.last_proj)/main_df.last_proj * 100

print ("[*] Generating optimal lineups")
optimizer.load_players(player_list)
player = optimizer.get_player_by_name('Garoppolo')
optimizer.add_player_to_lineup(player)
for lineup in optimizer.optimize(n=5):
    print (lineup)

print ("[*] Outputing data")
main_df.to_csv("players.csv", index=False, columns=['first_name', 'last_name', 'position', 'team', 'next_game', 'opp', 'o_u', 'total_score', 'salary_dk', 'salary_fd', 'projected', 'last_pts', 'last_proj', 'pct_change'])
