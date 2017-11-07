from ffapi import EspnFflClient
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
exp = EspnFflClient(223275)
this_week = 9
for week in range(this_week,this_week+1):
    for team in [1,2,6,8,9,10,12,13,14,15,16,17] :
        print week, team
        if team in M_Eff:
            if week in M_Eff[team]:
                break
        exp = EspnFflClient(223275).test(team,week)
        # print exp['boxscore']['teams'][0]['slots'][0]['player'].keys()
        if exp['boxscore']['teams'][0]['teamId'] == team:
            base = exp['boxscore']['teams'][0]
        else:
            base = exp['boxscore']['teams'][1]
        # print exp['boxscore']['teams'][0]['slots'][player]['player'].keys()
        # print base['slots'][10]['player']['eligibleSlotCategoryIds']
        possible = {}
        for i in range(0,16):
            positions = [roster_map[x] for x in base['slots'][i]['player']['eligibleSlotCategoryIds']]
            fname = base['slots'][i]['player']['firstName']
            lname = base['slots'][i]['player']['lastName']
            name = fname+" "+lname
            if base['slots'][i]['opponentProTeamId'] == -1:
                score = 0
            else:
                score = base['slots'][i]['currentPeriodRealStats']['appliedStatTotal']

            if i<9:
                act = 'ACTIVE'
            else:
                act = 'BENCH'

            possible.setdefault(positions[0], {})
            possible[positions[0]].setdefault(score,[])
            possible[positions[0]][score].append(name)
            # print act+" "+ str(positions[0])+" "+fname+" "+lname+": "+str(score)

        roster = ['QB','RB','RB','WR','WR','TE','FLEX','D/ST','K']
        # print possible
        #get optimum roster
        ideal_score=0
        for i, r in enumerate(roster):
            if r=='FLEX':
                maxscore = -10
                maxscore = max(possible['RB'].keys())
                pos = 'RB'
                if possible['WR'].keys()!=[] and max(possible['WR'].keys()) > maxscore:
                    maxscore = max(possible['WR'].keys())
                    pos = 'WR'
                if possible['TE'].keys()!=[] and max(possible['TE'].keys()) > maxscore:
                    maxscore = max(possible['TE'].keys())
                    pos = 'TE'

                ideal_score+=max(possible[pos].keys())
                roster[i] = possible[pos][max(possible[pos].keys())][0]

            else:
                ideal_score+=max(possible[r].keys())
                roster[i] = possible[r][max(possible[r].keys())].pop()
                if possible[r][max(possible[r].keys())]==[]:
                    del possible[r][max(possible[r].keys())]
        weff = base['appliedActiveRealTotal']/float(ideal_score)
        # print possible['RB'][max(possible['RB'].keys())]
        # del possible['RB'][max(possible['RB'].keys())]
        # print possible['RB']

        # print roster
        M_Eff.setdefault(team,{})
        M_Eff[team][week]= weff

print M_Eff


teams = {1:'Michael Koester', 2:"Zach Haywood", 6:"Johal Baez", 8:"Eric Begens", 9:"Benjamin Burnstine", 10:"Matt Goldman", 12:"Eric Wilson", 13:"Daniel Wossenu", 14:"Mohamed Somji", 15:"Andrew Frost", 16:"Joshua Bautz", 17:"Michael Goldman"}
print 'THIS WEEK'
for keys in M_Eff:
    print teams[keys] +': %.2f'%(sum(M_Eff[keys])*100)+ '%'

for keys in M_Eff:
    print teams[keys] +': %.2f'%(M_Eff[keys][this_week]*100)+ '%'

#
# for keys in M_Eff:
#     sum = 0
#     for keys2 in M_Eff[keys]:
#         sum +=M_Eff[keys][keys2]
#     sum = sum/13.0
#     print keys, str(sum)
