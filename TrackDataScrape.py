# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2, csv


def scrape(urls, opener):
    print "scrape"
    events = []
    raceCount = 0 # keeps track of the number of races being handled

    for url in urls:
        page = opener.open(url).read()
        soup = BeautifulSoup(page, "lxml")

        #set = soup.find("div","pager").find_next("div").find_all("a") # for multiple tabs
        set = soup.find("div","tablelist").find_all("a") # for a single tab


        for link in set:
            events.append("https://"+link.get("href")[2:])
            raceCount=raceCount+1

    print raceCount
    return events



def eventScrape(events, opener):
    print "eventScrape"
    races = []
    raceCount = 0

    for event in events:
        page = opener.open(event).read()
        soup = BeautifulSoup(page, "lxml")
        for a in soup.find_all("div","events")[0].find_all('a')[1:]:
                if (a.string.strip() =="400 Meters"):
                    races.append("https://"+a.get("href")[2:])
                    print a.get("href")[2:]
                    raceCount = raceCount + 1
                    print raceCount

        # Women's data had to be dealt with a try/except because not every
        # meet had women's races
        '''
        try:
            for a in soup.find_all("div","events")[1].find_all('a')[1:]:
                if (a.string.strip() =="400 Meters"):
                    races.append("https://"+a.get("href")[2:])
                    print a.get("href")[2:]
                    raceCount = raceCount + 1
                    print raceCount
        except:
            print "No women's event"
        '''

    print races
    return races

def dataScrape(races, opener):
    print "dataScrape"
    raceData = []
    raceCount = 0

    for race in races:
        page = opener.open(race).read()
        soup = BeautifulSoup(page, "lxml")

        # limits the scrape to only athletes that place in the race
        length = len(soup.find("div","topperformances").find("table").find_all("tr"))
        i = 1
        while ((i < length) and (soup.find("div","topperformances").find_all("tr")[i].find_all("td")[0].string.strip() != "") ):
            date = soup.find("ul","datelocation").find('span', text='Date:').next_sibling.strip()

            location = soup.find("ul","datelocation").find('span', text='Location:').next_sibling.strip()

            if (soup.find("div","topperformances").find_all("tr")[i].find_all("td")[1].find("a") == None):
                name = soup.find("div","topperformances").find_all("tr")[i].find_all("td")[1].string.strip()
            else:
                name = soup.find("div","topperformances").find_all("tr")[i].find_all("td")[1].find("a").string

            if (soup.find("div","topperformances").find_all("tr")[i].find_all("td")[3].find("a") == None):
                team = soup.find("div","topperformances").find_all("tr")[i].find_all("td")[3].string.strip()
            else:
                team = soup.find("div","topperformances").find_all("tr")[i].find_all("td")[3].find("a").string

            time = soup.find("div","topperformances").find_all("tr")[i].find_all("td")[4].string.strip()

            place = soup.find("div","topperformances").find_all("tr")[i].find_all("td")[0].string.replace(".","")

            # separation of information by one character to make information a single string
            raceData.append((date+"*"+location+"*"+name+"*"+team+"*"+time+"*"+place).encode('ascii', 'replace'))
            print date+"*"+location+"*"+name+"*"+team+"*"+time+"*"+place
            i = i +1
        raceCount = raceCount+1
        print raceCount

    return raceData


def createCSV(name, raceData):
    print "addedToCSV"

    f = open(name+".csv",'a')

    try:
        writer = csv.writer(f)
        writer.writerow( ('Date', 'Location', 'Name', 'Team', 'Time', 'Place') )
        for data in raceData:
            split = data.split("*",5)
            writer.writerow( (split[0], split[1], split[2], split[3], split[4], split[5]) )
    finally:
        f.close()

def main():

    # Urls of interest
    urls = ["https://www.tfrrs.org/results_search.html?page=0&month=12&sport=track&title=1&go=1&year=2013"]
            #"https://www.tfrrs.org/results_search.html?page=1&month=5&sport=track&title=1&go=1&year=2013"]
            #"https://www.tfrrs.org/results_search.html?page=2&month=3&sport=track&title=1&go=1&year=2013"]

    opener = urllib2.build_opener() # creates a URL opener
    opener.addheaders = [('User-agent', 'Mozilla/5.0')] # assigns the identity of the opener to Mozilla

    totalScrape = scrape(urls, opener) # scrapes all track meets in 2013
    events = eventScrape(totalScrape, opener) #scrapes all of the track meets with the 400M
    data = dataScrape(events, opener) #scrapes the date, location, name of athlete, team, race time, and place

    name = "W400MRunDec2013"
    createCSV(name, data) # makes a csv file from scraped data

if __name__ == '__main__':
    main()




