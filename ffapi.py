from espnff import League

leagueid = 223275
year = 2016
leag = League(leagueid ,year)


def get_sim_schedule(l_id,y):
    league = League(l_id,y)
    schedule = []
    for week in range(1,14):
        for each in league.scoreboard(week):
            schedule.append([str(each.home_team.owner),str(each.away_team.owner),each.home_score,each.away_score, week])
    return schedule
# print league.teams[1].schedule
# print league.scoreboard(week=None)
# for n in range(1, 14):
#
#     print 'Week', n, ": ", league.power_rankings(n)[0:7]

# print get_sim_schedule(223275, 2016)

################

import requests


def _fetch_league():
    params = {
        'leagueId': 223275,
        'seasonId': 2016
    }
    r = requests.get('%sleagueSettings' % ("http://games.espn.com/ffl/api/v2/",), params=params)
    # self.status = r.status_code
    data = r.json()

    print data['leaguesettings']
    # print data['leaguesettings'].keys()
    # for key in data['leaguesettings'].keys():
    #
    #     print key,'....',data['leaguesettings'][key]



class EspnFflClient:
    def __init__(self, league_id):
        self.leagueId = league_id
        self.ENDPOINT = 'http://games.espn.com/ffl/api/v2/'
        self.RAND = '00921504334023'

    def get_recent_activity(self, count=20):
        url = self.ENDPOINT + 'recentActivity?' + '?leagueId=' + str(self.leagueId) + '&count=' + str(
            count) + '&rand=' + self.RAND
        r = requests.get(url)
        return r.json()

    def get_player_info(self):
        url = self.ENDPOINT + 'playerInfo' + '?leagueId=' + str(self.leagueId) + '&rand=' + self.RAND
        r = requests.get(url)
        return r.json()


    def test(self,team,week):
        # url = self.ENDPOINT + 'scoreboard' + '?leagueId=' + str(self.leagueId) +'&scoringPeriodId=13'+'&seasonId=2016'+'&rand=' + self.RAND
        url = self.ENDPOINT + 'boxscore?leagueId=223275&teamId='+str(team)+'&scoringPeriodId='+str(week)+'&seasonId=2015' + '&rand=' + self.RAND
        r = requests.get(url)
        return r.json()

    # def test(self):
    #     url = self.ENDPOINT + 'playerInfo' + '?leagueId=' + str(self.leagueId) + '&rand=' + self.RAND
    #     r = requests.get(url)
    #     return r.json()

client = EspnFflClient(223275)
# print(client.get_recent_activity(20))
# print(client.get_player_info())
print client.test(13,13)


# _fetch_league()

# url = self.ENDPOINT + 'scoreboard' + '?leagueId=' + str(
#     self.leagueId) + '&scoringPeriodId=13' + '&seasonId=2016' + '&rand=' + self.RAND
