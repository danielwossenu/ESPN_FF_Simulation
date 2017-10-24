import csv
import numpy as np
import operator
import urllib2
# import FFScrap
# response = urllib2.urlopen("http://games.espn.com/ffl/schedule?leagueId=223275")
# source = response.read()
# the first week to start simulating
sim_start = 8

# number of simulations
trials = 100000.0

teams_ls = ["Daniel Wossenu", "Mohamed Somji", "eric begens", "Zach Haywood", "Eric Wilson", "Johal Baez", "andrew frost", "Joshua Bautz", "Benjamin Burnstine", "mike goldman", "Michael Koester", "Matt Goldman"]
teams_ll = [['Daniel Wossenu'], ['Mohamed Somji'], ['eric begens'], ['Zach Haywood'], ['Eric Wilson'], ['Johal Baez'], ['andrew frost'], ['Joshua Bautz'], ['Benjamin Burnstine'], ['mike goldman'], ['Michael Koester'], ['Matt Goldman']]
wins = dict()
playoffs = []

#initialize dictionary the value is (wins, [game scores], mean, stddev, playoffs %)
for x in teams_ls:
    wins[x] = [0, [], 0, 0, 0]

# read CSV file
with open("C:/Users/Daniel/Documents/GitHub/ESPN_FF_Simulation/2017_schedule_2.csv", 'rb') as f:
    reader = csv.reader(f)
    next(reader, None)
    mylist = list(reader)

# mylist = FFScrap.get_schedule(source)


# Turn number strings to int in mylist for both game scores and the week number
for game in mylist:
    game[2] = float(game[2])
    game[3] = float(game[3])
    game[4] = float(game[4])

# assign wins to each team in "wins" dictionary
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
    for x in playoffs[:6]:
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



# for sim in range(1,trials,1):
#     print "a"
assign_wins()
calc_mean_stddev()
reset_wins()


for sim in range (1,int(trials+1),1):
    if sim%1000 == 0:
        print sim
    for num, game in enumerate(mylist[(6*(sim_start-1)):]):
        #assign score from random number based on normal dist with mean and st dev
        mylist[6*(sim_start-1) + num][2] = int(np.random.normal(wins[game[0]][2], wins[game[0]][3]))
        mylist[6*(sim_start-1) + num][3] = int(np.random.normal(wins[game[1]][2], wins[game[1]][3]))
        # mylist[6*(sim_start-1) + num][2] = int(np.random.normal(90, 10))
        # mylist[6*(sim_start-1) + num][3] = int(np.random.normal(90, 10))

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
    print each, ('%.2f' % (wins[each][4]*100))+"%"

# print wins