import urllib2

response = urllib2.urlopen("http://games.espn.com/ffl/schedule?leagueId=223275")
source = response.read()


def scrap(position, page, startword, stopword):
    start = page.find(startword, position) + len(startword)
    end = page.find(stopword, start)
    return page[start:end], end+1
# spot in page


def get_schedule(page):
    schedule = []
    stop = 0


    while page.find("</a>WEEK ", stop) != -1:
        week, stop = scrap(stop, page, "</a>WEEK ", "<")
        next_week = page.find("</a>WEEK ", stop)
        po_start = page.find("PLAYOFFS")

        if next_week == -1:
            next_week = po_start

        while page.find("title=", stop) <  next_week and page.find("title=", stop) != -1 :
            team1, stop = scrap(page.find("title=", stop), page, "(" ,")")
            team2, stop = scrap(page.find("title=", stop), page, "(" ,")")

            if page.find("Preview") > next_week:
                score1, stop = scrap(stop, page, 'quick">', "-")
                score2, stop = scrap(stop, page, "", "<")
            else:
                score1 = "0"
                score2 = "0"

            schedule.append([team1, team2, score1, score2, week])



    return schedule

# print len(source)
# print get_schedule(source)
