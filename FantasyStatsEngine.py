from espnff import League
from ffapi import EspnFflClient
import numpy as np
import operator


class StatEngine:
    def __init__(self, league_id, year):
        self.league = League(league_id, year)
        self.exp = EspnFflClient(league_id, year)

        self.team_id_to_owner = {}
        self.team_owner_to_id = {}

        for team in self.league.teams:
            # print team.team_id
            self.team_id_to_owner[team.team_id] = team.owner
            self.team_owner_to_id[team.owner] = team.team_id


    def get_league_schedule(self, thru_week=100):
        schedule = {}
        for each in range(1, 14):
            schedule[each] = {'games': [], 'added': []}

        for team in self.league.teams:

            for week, opponent in enumerate(team.schedule):
                # print week+1, team.team_id, opponent.team_id, team.scores[week], team.scores[week] - team.mov[week]
                # print week + 1, team.owner, opponent.owner, team.scores[week], team.scores[week] - team.mov[week]

                if team.team_id not in schedule[week + 1]['added']:
                    if week + 1 > thru_week:
                        schedule[week + 1]['games'].append([team.team_id, opponent.team_id, 0, 0, float(week + 1)])
                    else:
                        schedule[week + 1]['games'].append(
                            [team.team_id, opponent.team_id, team.scores[week], team.scores[week] - team.mov[week],
                             float(week + 1)])
                    schedule[week + 1]['added'].append(team.team_id)
                    schedule[week + 1]['added'].append(opponent.team_id)

        return schedule

    def simulate_season(self, start_sim_at_week = 1, num_simulations=10000):
        schedule = self.get_league_schedule(start_sim_at_week-1)
        # print schedule
        mylist = []
        for week in schedule:
            for game in schedule[week]['games']:
                mylist.append(game)
        # print mylist
        wins = dict()
        playoffs = []

        # initialize dictionary the value is (wins, [game scores], mean, stddev, playoffs %)
        for x in schedule[1]['added']:
            wins[x] = [0, [], 0, 0, 0]

        def assign_wins():
            for game in mylist:
                if game[2] != 0:
                    if game[2] > game[3]:
                        wins[game[0]][0] += 1
                    elif game[2] == game[3]:
                        wins[game[0]][0] += .5
                        wins[game[1]][0] += .5
                    elif game[2] < game[3]:
                        wins[game[1]][0] += 1

                    # append team scores to "wins" dictionary
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
            playoffs.sort(key=operator.itemgetter(1, 2), reverse=True)

            # assign share to "wins" for making playoffs in each trial
            eric = 0
            for x in playoffs[:6]:
                wins[x[0]][4] += (1 / float(num_simulations))
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

        # for sim in range(1,num_simulations,1):
        #     print "a"
        assign_wins()
        calc_mean_stddev()
        reset_wins()

        for sim in range(1, int(num_simulations + 1), 1):
            if sim % 1000 == 0:
                print sim
            for num, game in enumerate(mylist[(6 * (start_sim_at_week - 1)):]):
                # assign score from random number based on normal dist with mean and st dev
                # mylist[6*(start_sim_at_week-1) + num][2] = int(np.random.normal(wins[game[0]][2], wins[game[0]][3]))
                # mylist[6*(start_sim_at_week-1) + num][3] = int(np.random.normal(wins[game[1]][2], wins[game[1]][3]))
                mylist[6 * (start_sim_at_week - 1) + num][2] = int(np.random.normal(100, 10))
                mylist[6 * (start_sim_at_week - 1) + num][3] = int(np.random.normal(100, 10))

            assign_wins()
            calc_playoffs()
            reset_wins()

            # # use this if statement in debug mode with a stop placed on line 93 to see possible paths for individual players
            # if wins['Matt Goldman'][4] !=0:
            #     for each in playoffs:
            #         print each[0],each[1]
            #     print "a"
            playoffs = []
        print "\nPlayoffs Chances"
        for each in wins:
            print str(self.team_id_to_owner[each]) + ":", ('%.2f' % (wins[each][4] * 100)) + "%"


    def managerial_effciency(self, for_week):
        roster_map = {
            0: 'QB',
            1: 'TQB',
            2: 'RB',
            3: 'RB/WR',
            4: 'WR',
            5: 'WR/TE',
            6: 'TE',
            7: 'OP',
            8: 'DT',
            9: 'DE',
            10: 'LB',
            11: 'DL',
            12: 'CB',
            13: 'S',
            14: 'DB',
            15: 'DP',
            16: 'D/ST',
            17: 'K',
            18: 'P',
            19: 'HC',
            20: 'BE',
            21: 'IR',
            22: '',
            23: 'RB/WR/TE'
        }
        M_Eff = {}
        for week in range(for_week, for_week + 1):
            for team in [1, 2, 6, 8, 9, 10, 12, 13, 14, 15, 16, 17]:
                # print week, team
                if team in M_Eff:
                    if week in M_Eff[team]:
                        break
                exp = self.exp.test(team, week)
                # print exp['boxscore']['teams'][0]['slots'][0]['player'].keys()
                if exp['boxscore']['teams'][0]['teamId'] == team:
                    base = exp['boxscore']['teams'][0]
                else:
                    base = exp['boxscore']['teams'][1]
                # print exp['boxscore']['teams'][0]['slots'][player]['player'].keys()
                # print base['slots'][10]['player']['eligibleSlotCategoryIds']
                possible = {}
                for i in range(0, 16):
                    positions = [roster_map[x] for x in base['slots'][i]['player']['eligibleSlotCategoryIds']]
                    fname = base['slots'][i]['player']['firstName']
                    lname = base['slots'][i]['player']['lastName']
                    name = fname + " " + lname
                    if base['slots'][i]['opponentProTeamId'] == -1:
                        score = 0
                    else:
                        score = base['slots'][i]['currentPeriodRealStats']['appliedStatTotal']

                    if i < 9:
                        act = 'ACTIVE'
                    else:
                        act = 'BENCH'

                    possible.setdefault(positions[0], {})
                    possible[positions[0]].setdefault(score, [])
                    possible[positions[0]][score].append(name)
                    # print act+" "+ str(positions[0])+" "+fname+" "+lname+": "+str(score)

                roster = ['QB', 'RB', 'RB', 'WR', 'WR', 'TE', 'FLEX', 'D/ST', 'K']
                # print possible
                # get optimum roster
                ideal_score = 0
                for i, r in enumerate(roster):
                    if r == 'FLEX':
                        maxscore = -10
                        maxscore = max(possible['RB'].keys())
                        pos = 'RB'
                        if possible['WR'].keys() != [] and max(possible['WR'].keys()) > maxscore:
                            maxscore = max(possible['WR'].keys())
                            pos = 'WR'
                        if possible['TE'].keys() != [] and max(possible['TE'].keys()) > maxscore:
                            maxscore = max(possible['TE'].keys())
                            pos = 'TE'

                        ideal_score += max(possible[pos].keys())
                        roster[i] = possible[pos][max(possible[pos].keys())][0]

                    else:
                        ideal_score += max(possible[r].keys())
                        roster[i] = possible[r][max(possible[r].keys())].pop()
                        if possible[r][max(possible[r].keys())] == []:
                            del possible[r][max(possible[r].keys())]
                weff = base['appliedActiveRealTotal'] / float(ideal_score)
                # print possible['RB'][max(possible['RB'].keys())]
                # del possible['RB'][max(possible['RB'].keys())]
                # print possible['RB']

                # print roster
                M_Eff.setdefault(team, {})
                M_Eff[team][week] = weff

        # print M_Eff

        print '\nManagerial Efficiency'

        for keys in M_Eff:
            print self.team_id_to_owner[keys] + ': %.2f' % (M_Eff[keys][for_week] * 100) + '%'

    def power_rankings(self, week):
        rankings = self.league.power_rankings(week)
        print "\nPower Rankings"
        for rank in rankings:
            print rank[1].owner, ":", rank[0]

if __name__ == "__main__":
    engine = StatEngine(223275, 2018)
    engine.simulate_season(2,1000)
    engine.managerial_effciency(1)
    engine.power_rankings(1)

