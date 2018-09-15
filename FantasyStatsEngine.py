from espnff import League
import numpy as np
import operator


class StatEngine:
    def __init__(self, league_id, year):
        self.league = League(league_id, year)

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
                print week + 1, team.owner, opponent.owner, team.scores[week], team.scores[week] - team.mov[week]

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
        mylist = []
        for week in schedule:
            for game in schedule[week]['games']:
                mylist.append(game)

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
                wins[x[0]][4] += (1 / num_simulations)
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
        for each in wins:
            print str(self.team_id_to_owner[each]) + ":", ('%.2f' % (wins[each][4] * 100)) + "%"



if __name__ == "__main__":
    engine = StatEngine(223275, 2018)
    print engine.simulate_season(2,1000)

