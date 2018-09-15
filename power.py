from espnff import League

leagueid = 223275
year = 2018
leag = League(leagueid ,year)

rankings = leag.power_rankings(9)

for rank in rankings:
    print rank[1],rank[0]