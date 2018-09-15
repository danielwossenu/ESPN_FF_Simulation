from espnff import League
import pickle
import numpy as np
import operator

# league_api = League(223275, 2017)
# with open('league2017.pkl', 'wb') as output:
#     pickle.dump(league_api, output, pickle.HIGHEST_PROTOCOL)



def get_schedule(year):

    with open('league{}.pkl'.format(year), 'rb') as input:
        league = pickle.load(input)
    schedule = {}

    thru_week = 100

    team_id_to_owner = {}
    team_owner_to_id = {}

    # for each in range(1,16):
    #     schedule[each]={'games':[],'added':[]}
    for team in league.teams:
        # print team.team_id
        team_id_to_owner[team.team_id] = team.owner
        team_owner_to_id[team.owner] = team.team_id
        for week,opponent in enumerate(team.schedule):
            if week+1 not in schedule:
                schedule[week+1] = {'games': [], 'added': []}
            # print week+1, team.team_id, opponent.team_id, team.scores[week], team.scores[week] - team.mov[week]
            # print week+1, team.owner, opponent.owner, team.scores[week], team.scores[week] - team.mov[week]

            if team.team_id not in schedule[week+1]['added']:
                if week+1 > thru_week:
                    schedule[week+1]['games'].append([team.team_id, opponent.team_id, 0, 0, float(week+1)])
                else:
                    schedule[week+1]['games'].append([team.team_id, opponent.team_id, team.scores[week], team.scores[week] - team.mov[week], float(week+1)])
                schedule[week+1]['added'].append(team.team_id)
                schedule[week+1]['added'].append(opponent.team_id)


    # print schedule
    mylist=[]
    for week in schedule:
        for game in schedule[week]['games']:
            mylist.append(game)

    return mylist, team_id_to_owner





overall_team_dict = {}
for i in range(1,20):
    overall_team_dict[1]=""
hth_record = np.zeros((20,20,3), dtype=np.int64)

for year in range(2011,2018):
    print year
    year_schedule, teams = get_schedule(year)
    for i in teams:
        overall_team_dict[i] = teams[i]

    for game in year_schedule:
       team1 = game[0] - 1
       team2 = game[1] - 1
       if team1 ==0 and team2 == 1:
           print 'a'
       score1 = game[2]
       score2 = game[3]

       if score1 > score2:
           hth_record[team1][team2][0] += 1
           hth_record[team2][team1][1] += 1
       elif score1 < score2:
           hth_record[team1][team2][1] += 1
           hth_record[team2][team1][0] += 1
       elif score1 == 0 and score2 == 0:
           continue
       elif score1 == score2:
           hth_record[team1][team2][2] += 1
           hth_record[team2][team1][2] += 1




np.savetxt("wins.csv", hth_record[:,:,0], delimiter=",")
np.savetxt("losses.csv", hth_record[:,:,1], delimiter=",")
np.savetxt("ties.csv", hth_record[:,:,2], delimiter=",")

# print hth_record
for x in range(1,20):
        if x not in overall_team_dict:
            print x
        else:
            print overall_team_dict[x]

