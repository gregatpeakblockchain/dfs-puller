import nflgame

def calf_defense():
    teams = [
                ['ARI', 'Arizona', 'Cardinals', 'Arizona Cardinals'],
                ['ATL', 'Atlanta', 'Falcons', 'Atlanta Falcons'],
                ['BAL', 'Baltimore', 'Ravens', 'Baltimore Ravens'],
                ['BUF', 'Buffalo', 'Bills', 'Buffalo Bills'],
                ['CAR', 'Carolina', 'Panthers', 'Carolina Panthers'],
                ['CHI', 'Chicago', 'Bears', 'Chicago Bears'],
                ['CIN', 'Cincinnati', 'Bengals', 'Cincinnati Bengals'],
                ['CLE', 'Cleveland', 'Browns', 'Cleveland Browns'],
                ['DAL', 'Dallas', 'Cowboys', 'Dallas Cowboys'],
                ['DEN', 'Denver', 'Broncos', 'Denver Broncos'],
                ['DET', 'Detroit', 'Lions', 'Detroit Lions'],
                ['GB', 'Green Bay', 'Packers', 'Green Bay Packers'],
                ['HOU', 'Houston', 'Texans', 'Houston Texans'],
                ['IND', 'Indianapolis', 'Colts', 'Indianapolis Colts'],
                ['JAX', 'Jacksonville', 'Jaguars', 'Jacksonville Jaguars'],
                ['KC', 'Kansas City', 'Chiefs', 'Kansas City Chiefs'],
                ['MIA', 'Miami', 'Dolphins', 'Miami Dolphins'],
                ['MIN', 'Minnesota', 'Vikings', 'Minnesota Vikings'],
                ['NE', 'New England', 'Patriots', 'New England Patriots'],
                ['NO', 'New Orleans', 'Saints', 'New Orleans Saints'],
                ['NYG', 'Giants', 'NY', 'New York Giants'],
                ['NYJ', 'Jets', 'NY', 'New York Jets'],
                ['OAK', 'Oakland', 'Raiders', 'Oakland Raiders'],
                ['PHI', 'Philadelphia', 'Eagles', 'Philadelphia Eagles'],
                ['PIT', 'Pittsburgh', 'Steelers', 'Pittsburgh Steelers'],
                ['SD', 'San Diego', 'Chargers', 'San Diego Chargers'],
                ['SEA', 'Seattle', 'Seahawks', 'Seattle Seahawks'],
                ['SF', 'San Francisco', '49ers', 'San Francisco 49ers'],
                ['LA', 'St. Louis', 'Rams', 'St. Louis Rams'],
                ['TB', 'Tampa Bay', 'Buccaneers', 'Tampa Bay Buccaneers'],
                ['TEN', 'Tennessee', 'Titans', 'Tennessee Titans'],
                ['WAS', 'Washington', 'Redskins', 'Washington Redskins']
        ]
    for game in games:
        print (game)

        # Sacks
        print ("SACKS")
        print game.players.defense().filter(home=True, defense_sk=lambda x: x >= 1)
        print game.players.defense().filter(home=False, defense_sk=lambda x: x >= 1)
        # Interceptions
        print ("INT")
        print game.players.defense().filter(home=True, defense_int=lambda x: x >= 1)
        print game.players.defense().filter(home=False, defense_int=lambda x: x >= 1)
        print ("INT TDS")
        print game.players.defense().filter(home=True, defense_int_tds=lambda x: x >= 1)
        print game.players.defense().filter(home=False, defense_int_tds=lambda x: x >= 1)
        print ("FUMBLE RECOVERY")
        print game.players.defense().filter(home=True, defense_frec=lambda x: x >= 1)
        print game.players.defense().filter(home=False, defense_frec=lambda x: x >= 1)
        print ("FUMBLE RECOVERY TD")
        print game.players.defense().filter(home=True, defense_frec_tds=lambda x: x >= 1)
        print game.players.defense().filter(home=False, defense_frec_tds=lambda x: x >= 1)  
        print ("MISC TD")
        print game.players.defense().filter(home=True, defense_misc_tds=lambda x: x >= 1)
        print game.players.defense().filter(home=False, defense_misc_tds=lambda x: x >= 1) 
        print ("BLOCKED PUNT")
        print game.players.defense().filter(home=True, defense_misc_tds=lambda x: x >= 1)
        print game.players.defense().filter(home=False, defense_misc_tds=lambda x: x >= 1) 
        print ("SAFETY")
        print game.players.defense().filter(home=True, defense_safe=lambda x: x >= 1)
        print game.players.defense().filter(home=False, defense_safe=lambda x: x >= 1) 
        print ("BLOCKED EXTRAPOINT")
        print game.players.defense().filter(home=True, defense_xpblk=lambda x: x >= 1)
        print game.players.defense().filter(home=False, defense_xpblk=lambda x: x >= 1) 

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

for game in games:
    print game

for player in sorted(players, key=lambda x: base_fantasy_points(x), reverse=True):
    if base_fantasy_points(player):
        try:
            print player.player.name, player.team, base_fantasy_points(player)
        except:
            continue
        #print player.formatted_stats()
