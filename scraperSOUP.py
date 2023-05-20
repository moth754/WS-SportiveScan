import requests
from bs4 import BeautifulSoup
import threading
from datetime import datetime
from time import sleep

now = datetime.now()

#array setups to store results and category prizes
RESULTurl = ["https://www.webscorer.com/racedetails?raceid=313058&did=382601"]
RESULTdistance = ["Spitfire"]
RESULTmedalcat = ["Senior - M","Senior - F","Vet 40 - M","Vet 40 - F"] #medal cat is defined as distance - category - gender
GOLDRESULTtimeMINS = [140,200,300,400]
SILVERRESULTtimeMINS = [300,400,600,800]

NUMBERS = []
NAMES = []
CATEGORIES = []
DISTANCES = []
GENDERS = []
MEDALCATS = []
MEDALS = []
TIMES = []
MINS = []

FIRSTRUN = 1


numberofdistances = len(RESULTdistance)

def get_data_question():
    if FIRSTRUN == 1:
        print("Loading intial data....")
        try:
            pull_data()
            print("Data pull successfull")
        except:
            "Data pull error"
    else:    
        while True:
            now = datetime.now()
            current_secs = now.strftime("%S")
            if current_secs == "00":
                pull_data()
            else:
                sleep(0.5)

def pull_data():
    for i in range(numberofdistances):
        url = RESULTurl[i]
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        response = requests.get(url, headers=headers)
        #print(response.status_code)

        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find('table', class_ = 'results-table nolaps')

        NUMBERS = []
        NAMES = []
        CATEGORIES = []
        DISTANCES = []
        GENDERS = []
        MEDALCATS = []
        MEDALS = []
        TIMES = []
        MINS = []

        #print(table)

        for race_data in table.find_all('tbody'): #parse the data into rows
            rows = race_data.find_all('tr')
            #print(rows)

        for row in rows: #pull out each competitors records
            #find numbers
            RAWnumber = row.find_all('td')[1].text
            #print(RAWnumber)
            NUMBERS.append(RAWnumber)
            #find names
            RAWname = row.find_all('td')[2].text
            #print(RAWname)
            NAMES.append(RAWname)
            #find categories
            RAWcategory = row.find_all('td')[3].text
            #print(RAWcategory)
            CATEGORIES.append(RAWcategory)
            #find gender
            RAWgender = row.find_all('td')[5].text
            #print(RAWgender)
            GENDERS.append(RAWgender)
            #find time
            RAWtime = row.find_all('td')[6].text
            #print(RAWtime)
            TIMES.append(RAWtime)
            RAWmins = RAWtime.split(":")
            if len(RAWmins) == 3:
                RAWmins = int(RAWmins[0])*60 + int(RAWmins[1])
                MINS.append(RAWmins)
            elif len(RAWmins) == 2:
                RAWmins = int(RAWmins[1])
                MINS.append(RAWmins)
            else:
                RAWmins = 0
            #add in the distance
            DISTANCES.append(RESULTdistance[i])
            #find medal category
            RAWmedalcat = RAWcategory + " - " + RAWgender
            MEDALCATS.append(RAWmedalcat)

            #find medal colour
            try:
                wheretolook = RESULTmedalcat.index(RAWmedalcat)
                goldcutoff = GOLDRESULTtimeMINS[wheretolook]
                silvercutoff = SILVERRESULTtimeMINS[wheretolook]

                if RAWmins <= goldcutoff:
                    RAWmedal = "Gold"
                elif RAWmins <= silvercutoff:
                    RAWmedal = "Silver"
                else:
                    RAWmedal = "Bronze"
            except:
                RAWmedal = "Category not found"
            MEDALS.append(RAWmedal)

        QUANTITY = len(NUMBERS) #how many numbers in total

def display_data():
    while True():
        search = input("Enter the number you a looking for and press enter: ")
        try:
            DISPLAYwheretolook = NUMBERS.index(search)
            DISPLAYname = NAMES[DISPLAYwheretolook]
            DISPLAYmedalcat = MEDALCATS[DISPLAYwheretolook]
            DISPLAYdistance = DISTANCES[DISPLAYwheretolook]
            DISPLAYtime = TIMES[DISPLAYwheretolook]
            DISPAYmedal = MEDALS[DISPLAYwheretolook]
            print("")
            print("Bib: " + search)
            print("Name & Team: " + DISPLAYname)
            print("Category & Gender: " + DISPLAYmedalcat)
            print("Distance: " + DISPLAYdistance)
            print("Medal: " + DISPAYmedal)
            print()

        #need to add display code

        except:
            print("Not found - speak to timing if no typo in number")
        
        print("")
        print("")

#get_data()
#display_data()

background = threading.Thread(target=get_data_question)
background.start()


gui = threading.Thread(target=display_data)
gui.start()
