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


#########   Settings   #########

# number of nodes and arcs
NUMBER_OF_PEOPLE = 500
NUMBER_OF_CONTACTS = 1500
NUMBER_OF_PLACES = 20
NUMBER_OF_ROOMS = 50
NUMBER_OF_VISITS = 1000

# datetime related to COVID
min_datetime = datetime(2020, 1, 1, 0, 0, 0)
min_positive_datetime = datetime.now() - relativedelta(days=45)
max_datetime = datetime.now()

# datetime related to birth
birth_min_datetime = datetime(1950, 1, 1, 0, 0, 0)
birth_max_datetime = datetime.now() - relativedelta(years=18)

# probability ratio
positive_ratio = 0.08
risky_ratio = 0.1

# number of tests per person
max_tests = 10

# duration of contacts/visits in minutes
min_contact_duration = 10  
max_contact_duration = 1439  

min_visit_duration = 5  
max_visit_duration = 720  

# max capience of a room
max_capience = 150

# filepaths
cities_filepath = './data/Comuni-Italiani.csv'
places_filepath = './data/Luoghi-Italiani.csv'

#########   Functions   #########

# Save list of dictionaries to CSV
def saveCSV(toCSV, filename) -> None:

    keys = toCSV[0].keys()
    with open(f'output/{filename}', 'w', newline='')  as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(toCSV)

# Generate random italian phone number in string format
def randomPhone() -> str:

    phone_number = '3'
    phone_number += str(random.randint(2, 5))
    
    for i in range(1, 9):
        phone_number += str(random.randint(0, 9))

    return phone_number

# Generate random Room Name format: #ASCIILetter.#Digit.#Digit
def randomRoomName() -> str:

    S = random.choice(string.ascii_letters).upper() + '.' + str(random.randint(0,9)) + '.' + str(random.randint(0,9))

    return S


# Assert Place has rooms
def hasRooms(place):

    places_with_rooms = ['populated place', 'palace', 'church', 'hotel', 'school']

    return place in places_with_rooms 


# Generate rooms from places
def generateRooms(places) -> list:

    rooms = []
    current_place = {'Type': None}

    for i in range(NUMBER_OF_ROOMS):
        while not(hasRooms(current_place['Type'])):
            current_place = places[random.randint(0,len(places) - 1)]

        room_name = randomRoomName()
        capience = random.randint(0, max_capience - 1)
        rooms.append({
                'Code': current_place['Code'],
                'Name': room_name,
                'Capience': capience
            })
        current_place = {'Type': None}

    return rooms


# Return Entities in list of dictionaries format
def getEntities() -> (list, list, list, list, list, list):

    people = []
    places = []
    rooms = []
    medical_records = []
    covid_vaccines = []
    covid_tests = []
    places_df = pd.read_csv(places_filepath, sep=';')
    cities_df = pd.read_csv(cities_filepath, header = 1, sep=';')
    cities = cities_df['Denominazione in italiano']
    del cities_df

    for i in range(NUMBER_OF_PEOPLE):

        ### Person Info ####

        sex = random.choice(['male','female'])
        first_name = names.get_first_name(gender=sex)
        last_name = names.get_last_name()
        positive = np.random.choice([True, False], p=[positive_ratio, 1 - positive_ratio])
        birth = (birth_min_datetime + (birth_max_datetime - birth_min_datetime) * random.random()).strftime('%d/%m/%Y')
        phone_number = randomPhone()
        mail_provider  = random.choice(['gmail.com','outlook.it','icloud.com','hotmail.it','yahoo.it'])
        email = f'{first_name.lower()}.{last_name.lower()}@{mail_provider}'
        if positive:
            last_confirm = (min_positive_datetime + (max_datetime - min_positive_datetime) * random.random()).strftime('%d/%m/%Y')
        else:
            last_confirm = random.choice([None, (min_datetime + (max_datetime - min_datetime) * random.random()).strftime('%d/%m/%Y')])

        sex = sex[0].upper()
        birthplace = cities[random.randint(0,len(cities)-1)]

        try:
            CIF = codicefiscale.encode(surname=last_name, name=first_name, sex=sex, birthdate=birth, birthplace=birthplace)
        except:
            continue

        covid_vaccinated = random.choice([True, False])
        risky_subject = np.random.choice([True, False], p=[risky_ratio, 1 - risky_ratio])
        health_status = random.choice(["bad", "average", "good"])
        
        ### ###

        people.append({
            'CIF': CIF,
            'First_Name': first_name,
            'Last_Name': last_name,
            'Positive': positive,
            'Birth': birth,
            'Birthplace': birthplace,
            'Phone_Number': phone_number,
            'Email': email,
            'Last_Confirm': last_confirm,
            'Sex': sex
            })

        medical_records.append({
                'CIF': CIF,
                'Covid_Vaccinated': covid_vaccinated,
                'Risky_Subject': risky_subject,
                'Health_Status': health_status,
            })


        # Max 2 Vaccines per person
        if (covid_vaccinated):
                for i in range(random.randint(1,2)):
                    covid_vaccines.append({
                        'CIF': CIF,
                        'Date': (min_datetime + (max_datetime - min_datetime) * random.random()).strftime('%d/%m/%Y'),
                        'Type': random.choice(["Pfizer", "Moderna", "Astrazeneca", "Johnson & Johnson"])
                    })

        # At leats one test if last_confirm (with the same result as Person.Positive)
        if (last_confirm):
            covid_tests.append({
                'CIF': CIF,
                'Date': last_confirm,
                'Result': positive,
            })

            #Discrete ~Normal Distribution~ centered in 0 describing number of test per person
            x = np.arange(0, max_tests)
            xU, xL = x + 0.5, x - 0.5 
            prob = ss.norm.cdf(xU, scale = 3) - ss.norm.cdf(xL, scale = 3)
            prob = prob / prob.sum() 
            num = np.random.choice(x, p=prob)

            for i in range(num):
                covid_tests.append({
                    'CIF': CIF,
                    'Date': (min_datetime + (datetime.strptime(last_confirm,'%d/%m/%Y') - min_datetime) * random.random()).strftime('%d/%m/%Y'),
                    'Result': positive,
                })

    
    n = len(places_df)
    idxs = np.zeros(n)

    # Get #NUMBER_OF_PLACES random places
    for i in range (NUMBER_OF_PLACES):
      l = random.randint(0,n)
      idxs[l] = places_df['Code'][l]

    places = places_df[places_df['Code'] == idxs].to_dict('records')
    del places_df

    # Generate Rooms
    rooms  = generateRooms(places)

    return people, medical_records, covid_vaccines, covid_tests, places, rooms


# Generate Relations
def getRelations(people, places, rooms):

    contacts = []
    visits =  []
    lives = []

    # Generate Contacts
    for i in range(NUMBER_OF_CONTACTS):

        contact_date = (min_datetime + (max_datetime - min_datetime) * random.random()).strftime('%d/%m/%Y')
        contact_duration = str(timedelta(minutes=random.randint(min_contact_duration, max_contact_duration)))

        P1 = random.randint(0, NUMBER_OF_PEOPLE - 1) 
        P2 = random.randint(0, NUMBER_OF_PEOPLE - 1)

        # No contact with itself
        if P1 == P2:
            P2 -= 1

        contacts.append(
            {
                'CIF1': people[P1]['CIF'],
                'CIF2': people[P2]['CIF'],
                'Date': contact_date,
                'Duration': contact_duration
            })

    # Generate Visits
    for i in range(NUMBER_OF_VISITS):

        visit_date = (min_datetime + (max_datetime - min_datetime) * random.random()).strftime('%d/%m/%Y')
        visit_duration = str(timedelta(minutes=random.randint(min_visit_duration, max_visit_duration)))

        person = random.randint(0, NUMBER_OF_PEOPLE - 1)
        room = random.choice([None, random.randint(0, NUMBER_OF_ROOMS - 1)])

        # If the place has no Rooms
        if room is None:
            place = places[random.randint(0, NUMBER_OF_PLACES - 1)]
            while hasRooms(place['Type']):
                place = places[random.randint(0, NUMBER_OF_PLACES - 1)]

            visits.append(
            {
                'CIF': people[person]['CIF'],
                'Place': place['Code'],
                'Room': None,
                'Date': visit_date,
                'Duration': visit_duration

            })

        else:
            visits.append(
            {
                'CIF': people[person]['CIF'],
                'Place': rooms[room]['Code'],
                'Room': rooms[room]['Name'],
                'Date': visit_date,
                'Duration': visit_duration
            })
        
    # Generate Lives
    for i in range(NUMBER_OF_PEOPLE):

        place = places[random.randint(0,len(places)-1)]

        lives.append(
            {
                'CIF': people[i]['CIF'],
                'Code': place['Code']
            })


    return contacts, visits, lives



if __name__ == "__main__":

    people, medical_records, covid_vaccines, covid_tests, places, rooms = getEntities()
    
    #update counts
    NUMBER_OF_PEOPLE = len(people)
    NUMBER_OF_PLACES = len(places)

    contacts, visits, lives = getRelations(people, places, rooms)

    saveCSV(people, 'people.csv')
    saveCSV(medical_records, 'medical_records.csv')
    saveCSV(covid_vaccines, 'covid_vaccines.csv')
    saveCSV(covid_tests, 'covid_tests.csv')
    saveCSV(places, 'places.csv')
    saveCSV(rooms, 'rooms.csv')

    saveCSV(lives, 'lives.csv')
    saveCSV(contacts, 'contacts.csv')
    saveCSV(visits, 'visits.csv')
