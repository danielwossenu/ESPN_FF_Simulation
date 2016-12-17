import numpy as np
import operator
from espnff import League

# my league 223275 (12 team, 1 division, 6 playoffs teams)
# league 2223273 (10 teams, 2 divisions, 4 playoff teams)


def simulate(league_number, year):
    #initialize wins dictionary and playoffs list
    wins = dict()
    playoffs = []

    # league_number is league id from ESPN
    # league_number = 223275

    # the first week to start simulating
    sim_start = 13

    # number of simulations
    trials = 1000.0

    # create League object from espnff package
    league = League(league_number, year)

    # assign relevant information to variables
    team_count = league.settings.team_count
    playoff_tiebreaker = league.settings.playoff_seed_tie_rule
    matchup_tiebreaker = league.settings.tie_rule
    po_team_count = league.settings.playoff_team_count
    reg_weeks = league.settings.reg_season_count


    #create schedule
    schedule = []
    for week in range(1, reg_weeks+1):
        for each in league.scoreboard(week):
            schedule.append(
                [str(each.home_team.owner), str(each.away_team.owner), each.home_score, each.away_score, week])

    # create a list of strings that are the team names
    teams_ls=[]
    for game in schedule:
        if game[4] == "1" or game[4] == 1:
            team1 = game[0]
            team2 = game[1]
            s1 = ""
            s2 = ""
            for c in team1:
                s1 = s1+c
            for c in team2:
                s2 = s2+c
            teams_ls.append(s1)
            teams_ls.append(s2)
        else:
            break


    # initialize dictionary the value is (wins, [game scores], mean, stddev, playoffs %)
    for x in teams_ls:
        wins[x] = [0, [], 0, 0, 0]

    # Turn number strings to int in schedule for both game scores and the week number
    # for game in schedule:
    #     game[2] = int(game[2])
    #     game[3] = int(game[3])
    #     game[4] = int(game[4])

    # assign wins to each team in "wins" dictionary
    def assign_wins():
        for game in schedule:
            if game[2] != 0:
                if game[2] > game[3]:
                    wins[game[0]][0] += 1
                elif game[2] == game[3]:
                    # if matchup tiebreaker = none
                    wins[game[0]][0] += .5
                    wins[game[1]][0] += .5
                elif game[2] < game[3]:
                    wins[game[1]][0] += 1

                #append team scores to "wins" dictionary
                wins[game[0]][1].append(game[2])
                wins[game[1]][1].append(game[3])

    def calc_mean_stddev():
        for key in wins:
            wins[key][2] = np.mean(wins[key][1])
            wins[key][3] = np.std(wins[key][1])

    def calc_playoffs():
        # sort by wins and then total points
        for key in wins:
            playoffs.append([key, wins[key][0], sum(wins[key][1])])
        playoffs.sort(key=operator.itemgetter(1,2), reverse=True)

        # assign share to "wins" for making playoffs in each trial
        eric = 0
        for x in playoffs[:po_team_count]:
            wins[x[0]][4] += (1/trials)
        #     if x[0] == "Eric Wilson":
        #         eric =1
        # if eric == 0:
        #     for each in playoffs:
        #         print each[0],each[1]
        #     print "a"

        # print playoffs


    def reset_wins():
        for y in wins:
            wins[y][0] = 0
            wins[y][1] = []

    assign_wins()
    calc_mean_stddev()
    reset_wins()


    for sim in range (1,int(trials+1),1):
        # the number 6 in the next line should be replaced by the # of teams in the league divided by 2
        for num, game in enumerate(schedule[(6*(sim_start-1)):]):
            #assign score from random number based on normal dist with mean and st dev
            # schedule[53 + num][2] = int(np.random.normal(wins[game[0]][2], wins[game[0]][3]))
            # schedule[53 + num][3] = int(np.random.normal(wins[game[1]][2], wins[game[1]][3]))
            schedule[6*(sim_start-1) + num][2] = int(np.random.normal(90, 10))
            schedule[6*(sim_start-1) + num][3] = int(np.random.normal(90, 10))

        assign_wins()
        calc_playoffs()
        reset_wins()


        # # use this if statement in debug mode with a stop placed on line 93 to see possible paths for individual players
        # if wins['Matt Goldman'][4] !=0:
        #     for each in playoffs:
        #         print each[0],each[1]
        #     print "a"
        playoffs = []

    results = []
    for each in wins:
        results.append([each, wins[each][4]*100])
    return results

a = simulate(223275, 2016)

for each in a:
    print each[0], each[1]
