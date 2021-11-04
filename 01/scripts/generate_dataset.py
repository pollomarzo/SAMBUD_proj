import names
import random
import numpy as np
import csv
import string

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from codicefiscale import codicefiscale
import scipy.stats as ss
import pandas as pd


### Settings ###

NUMBER_OF_PEOPLE = 200
CONTACTS = 100
NUMBER_OF_PLACES = 100
NUMBER_OF_ROOMS = 50
NUMBER_OF_VISITS = 100

min_datetime = datetime(2020, 1, 1, 0, 0, 0)
min_positive_datetime = datetime.now() - relativedelta(days=45)
max_datetime = datetime.now()

birth_min_datetime = datetime(1950, 1, 1, 0, 0, 0)
birth_max_datetime = datetime.now() - relativedelta(years=18)

positive_ratio = 0.08
risky_ratio = 0.1

max_tests = 10

min_contact_duration = 10  ##minutes
max_contact_duration = 1439  

min_visit_duration = 5  ##minutes
max_visit_duration = 720  

max_capience = 150

### Functions ###


def saveCSV(toCSV, filename) -> None:

    keys = toCSV[0].keys()
    with open(f'output/{filename}', 'w', newline='')  as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(toCSV)

def randomPhone() -> str:

    phone_number = '3'
    phone_number += str(random.randint(2, 5))
    
    for i in range(1, 9):
        phone_number += str(random.randint(0, 9))

    return phone_number

def randomRoomName() -> str:

    S = random.choice(string.ascii_letters).upper() + '.' + str(random.randint(0,9)) + '.' + str(random.randint(0,9))

    return S

def hasRooms(place):

    places_with_rooms = ['populated place', 'palace', 'church', 'hotel', 'school']

    return place in places_with_rooms 


def generateRooms(places) -> list:

    rooms = []
    current_place = {'type': None}

    for i in range(NUMBER_OF_ROOMS):
        while not(hasRooms(current_place['type'])):
            current_place = places[random.randint(0,len(places) - 1)]

        room_name = randomRoomName()
        capience = random.randint(0, max_capience - 1)
        rooms.append({
                'Place': current_place['code'],
                'Name': room_name,
                'Capience': capience
            })
        current_place = {'type': None}

    return rooms

def getEntities() -> (list, list, list, list, list, list):

    people = []
    places = []
    rooms = []
    medical_records = []
    covid_vaccines = []
    covid_tests = []
    df = pd.read_csv('data/Comuni-Italiani.csv', header = 1, sep=';')
    cities = df['Denominazione in italiano']
    del df

    for i in range(NUMBER_OF_PEOPLE):

        ### Person Info ####

        first_name = names.get_first_name()
        last_name = names.get_last_name()
        positive = np.random.choice([True, False], p=[positive_ratio, 1 - positive_ratio])
        birth = (birth_min_datetime + (birth_max_datetime - birth_min_datetime) * random.random()).strftime('%d/%m/%Y')
        phone_number = randomPhone()
        email = f'{first_name.lower()}.{last_name.lower()}@gmail.com'
        if positive:
            last_confirm = (min_positive_datetime + (max_datetime - min_positive_datetime) * random.random()).strftime('%d/%m/%Y')
        else:
            last_confirm = random.choice([None, (min_datetime + (max_datetime - min_datetime) * random.random()).strftime('%d/%m/%Y')])

        sex = random.choice(['M','F'])
        birthplace = cities[random.randint(0,len(cities)-1)]

        try:
            CFI = codicefiscale.encode(surname=last_name, name=first_name, sex=sex, birthdate=birth, birthplace=birthplace)
        except:
            continue

        covid_vaccinated = random.choice([True, False])
        risky_subject = np.random.choice([True, False], p=[risky_ratio, 1 - risky_ratio])
        health_status = random.choice(["bad", "average", "good"])
        
        ### ###

        people.append({
            'CFI': CFI,
            'first_name': first_name,
            'last_name': last_name,
            'positive': positive,
            'birth': birth,
            'birthplace': birthplace,
            'phone_number': phone_number,
            'email': email,
            'last_confirm': last_confirm,
            'sex': sex
            })

        medical_records.append({
                'CFI': CFI,
                'covid_vaccinated': covid_vaccinated,
                'risky_subject': risky_subject,
                'health_status': health_status,
            })


        if (covid_vaccinated):
                for i in range(random.randint(1,2)):
                    covid_vaccines.append({
                        'CFI': CFI,
                        'date': (min_datetime + (max_datetime - min_datetime) * random.random()).strftime('%d/%m/%Y'),
                        'type': random.choice(["Pfizer", "Moderna", "Astrazeneca", "Johnson & Johnson"])
                    })

        
        if (last_confirm):
            covid_tests.append({
                'CFI': CFI,
                'date': last_confirm,
                'result': positive,
            })

            #Discrete ~Normal Distribution~ centered in 0
            x = np.arange(0, max_tests)
            xU, xL = x + 0.5, x - 0.5 
            prob = ss.norm.cdf(xU, scale = 3) - ss.norm.cdf(xL, scale = 3)
            prob = prob / prob.sum() 
            num = np.random.choice(x, p=prob)

            for i in range(num):
                covid_tests.append({
                    'CFI': CFI,
                    'date': (min_datetime + (datetime.strptime(last_confirm,'%d/%m/%Y') - min_datetime) * random.random()).strftime('%d/%m/%Y'),
                    'result': positive,
                })


    places_df = pd.read_csv("data/Luoghi-Italiani.csv")
    
    n = len(places_df)
    idxs = np.zeros(n)

    for i in range (NUMBER_OF_PLACES):
      l = random.randint(0,n)
      idxs[l] = places_df['code'][l]

    places = places_df[places_df['code'] == idxs].to_dict('records')


    rooms  = generateRooms(places)

    return people, medical_records, covid_vaccines, covid_tests, places, rooms



def getRelations(people, places, rooms):

    contacts = []
    visits =  []

    for i in range(CONTACTS):

        contact_date = (min_datetime + (max_datetime - min_datetime) * random.random()).strftime('%d/%m/%Y')
        contact_duration = str(timedelta(minutes=random.randint(min_contact_duration, max_contact_duration)))

        P1 = random.randint(0, NUMBER_OF_PEOPLE - 1) 
        P2 = random.randint(0, NUMBER_OF_PEOPLE - 1)

        if P1 == P2:
            P2 -= 1

        contacts.append(
            {
                'CFI1': people[P1]['CFI'],
                'CFI2': people[P2]['CFI'],
                'date': contact_date,
                'duration': contact_duration
            })

    for i in range(NUMBER_OF_VISITS):

        visit_date = (min_datetime + (max_datetime - min_datetime) * random.random()).strftime('%d/%m/%Y')
        visit_duration = str(timedelta(minutes=random.randint(min_visit_duration, max_visit_duration)))

        person = random.randint(0, NUMBER_OF_PEOPLE - 1)
        room = random.choice([None, random.randint(0, NUMBER_OF_ROOMS - 1)])


        if room is None:
            place = places[random.randint(0, NUMBER_OF_PLACES - 1)]
            while hasRooms(place['type']):
                place = places[random.randint(0, NUMBER_OF_PLACES - 1)]

            visits.append(
            {
                'CFI': people[person]['CFI'],
                'Place': place['code'],
                'Room': None,
                'Date': visit_date,
                'Duration': visit_duration

            })

        else:
            visits.append(
            {
                'CFI': people[person]['CFI'],
                'Place': rooms[room]['Place'],
                'Room': rooms[room]['Name'],
                'Date': visit_date,
                'Duration': visit_duration
            })
        


    return contacts, visits



if __name__ == "__main__":

    people, medical_records, covid_vaccines, covid_tests, places, rooms = getEntities()
    
    contacts, visits = getRelations(people, places, rooms)

    saveCSV(people, 'people.csv')
    saveCSV(medical_records, 'medical_records.csv')
    saveCSV(covid_vaccines, 'covid_vaccines.csv')
    saveCSV(covid_tests, 'covid_tests.csv')
    saveCSV(places, 'places.csv')
    saveCSV(rooms, 'rooms.csv')

    saveCSV(contacts, 'contacts.csv')
    saveCSV(visits, 'visits.csv')
