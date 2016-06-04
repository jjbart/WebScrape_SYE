__author__ = 'josiahbartlett'

from bs4 import BeautifulSoup
import urllib2, csv


def scrape(url,opener):
    print "scrape"
    game = []

    #opener = urllib2.build_opener()
    #opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    page = opener.open(url).read()
    soup = BeautifulSoup(page, "lxml")
    name = str(soup.find("title").string.strip().split(" ")[soup.find("title").string.strip().split(" ").index("vs")+1])
    year = str(soup.find("title").string.strip().split(" ")[-1].split("/")[-1])
    date = str(soup.find("title").string.strip().split(" ")[-1].replace("/","-"))

    i = 1
    while True:
        if type(soup.find(id="set-"+str(i))) == type(None) :
            break
        print "set"+str(i)
        set= soup.find(id="set-"+str(i)).find("table","play-by-play").tbody.find_all("td","hide-on-large text-center")


        for play in set:
            if play.string.strip() != "":
                game.append(play.string.strip().replace("-", ",") + ","+ str(i) + "," + name + "," + year)

        i += 1

    return (game,name,date)

def addHeader(name):
    f = open(name,'a')
    try:
        writer = csv.writer(f)
        writer.writerow( ('SLU Score', 'Opponent Score', 'Set', 'Opponent', 'Year') )
    finally:
        f.close()

def makeCSV(game,name,date):
    print "addedToCSV"

    f = open(name+date+".csv",'a')

    try:
        writer = csv.writer(f)
        writer.writerow( ('SLU Score', 'Opponent Score', 'Set', 'Opponent', 'Year') )
        for play in game:
            split = play.split(",",4)
            writer.writerow( (split[0], split[1], split[2], split[3], split[4]) )
    finally:
        f.close()

def allInOneCSV(game):
    name =  "SaintsVolleyball"
    f = open(name+".csv",'a')

    try:
        writer = csv.writer(f)
        for play in game:
            split = play.split(",",4)
            writer.writerow((split[0], split[1], split[2], split[3], split[4]))
    finally:
        f.close()



def main():

    # Urls of interest
    urls = ['http://www.saintsathletics.com/boxscore.aspx?path=wvball&id=4783',
            'http://www.saintsathletics.com/boxscore.aspx?path=wvball&id=4784',
            'http://www.saintsathletics.com/boxscore.aspx?path=wvball&id=4785',
            'http://www.saintsathletics.com/boxscore.aspx?path=wvball&id=4786',
            'http://www.saintsathletics.com/boxscore.aspx?path=wvball&id=4791',
            'http://www.saintsathletics.com/boxscore.aspx?path=wvball&id=4792',
            'http://www.saintsathletics.com/boxscore.aspx?path=wvball&id=4793',
            'http://www.saintsathletics.com/boxscore.aspx?path=wvball&id=4800',
            'http://www.saintsathletics.com/boxscore.aspx?path=wvball&id=4801',
            'http://www.saintsathletics.com/boxscore.aspx?path=wvball&id=4803',
            'http://www.saintsathletics.com/boxscore.aspx?path=wvball&id=4868',
            'http://www.saintsathletics.com/boxscore.aspx?path=wvball&id=5464',
            'http://www.saintsathletics.com/boxscore.aspx?path=wvball&id=5465',
            'http://www.saintsathletics.com/boxscore.aspx?path=wvball&id=5466',
            'http://www.saintsathletics.com/boxscore.aspx?path=wvball&id=5467',
            'http://www.saintsathletics.com/boxscore.aspx?path=wvball&id=5470']

    addHeader("SaintsVolleyball.csv") # creates header for csv file


    opener = urllib2.build_opener() # creates a URL opener
    opener.addheaders = [('User-agent', 'Mozilla/5.0')] # assigns the identity of the opener to Mozilla

    for url in urls:
        print url
        (game,name,date) = scrape(url, opener) # scrapes game data from a url
        makeCSV(game,name,date) # creates a separate csv file for each game
        allInOneCSV(game) # creates one csv file with data from all the scraped games

if __name__ == '__main__':
    main()
