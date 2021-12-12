import names
import pandas as pd
import scipy.stats as ss
import json

from codicefiscale import codicefiscale
from numpy import random as random
from numpy import arange
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


NUMBER_OF_CERTIFICATES = 10000

max_tests = 10
max_vaccines = 3
max_nurses = 5

# ratios
positive_ratio = 0.1

# datetime related to birth
birth_min_datetime = datetime(1950, 1, 1, 0, 0, 0)
birth_max_datetime = datetime.now() - relativedelta(years=18)

# datetime related to COVID
min_datetime = datetime(2020, 1, 1, 0, 0, 0)
max_datetime = datetime.now()

# datetime related to expiration date
min_expiration_v1 = datetime(2020, 10, 1, 0, 0, 0)
min_expiration_v2 = datetime(2020, 10, 1, 0, 0, 0) + relativedelta(years=1)
min_expiration_v3 = datetime(2020, 10, 1, 0, 0, 0) + relativedelta(years=2)

max_expiration_v1 = datetime.now()
max_expiration_v2 = datetime.now() + relativedelta(years=1)
max_expiration_v3 = datetime.now() + relativedelta(years=5)

# Datasets
cities_filepath = './data/Comuni-Italiani.csv'
cities_df = pd.read_csv(cities_filepath, header = 1, sep=';')
cities = cities_df['Denominazione in italiano']

places_filepath = './data/places.csv'
places_df = pd.read_csv(places_filepath)
num_places = len(places_df)


# Export to JSON function
def saveJSON(file, filepath):

    jsonString = json.dumps(file, indent=2)
    jsonFile = open(filepath, "w")
    jsonFile.write(jsonString)
    jsonFile.close()

# Return certificate validity 
def getValidity() -> list:

    validity = dict()
    version = random.choice(['v1','v2','v3'])

    if(version == 'v1'):
        max_expiration = max_expiration_v1
        min_expiration = min_expiration_v1
    elif(version == 'v2'):
        max_expiration = max_expiration_v2
        min_expiration = min_expiration_v2
    else:
        max_expiration = max_expiration_v3
        min_expiration = min_expiration_v3

    expiration_date = (min_expiration + (max_expiration - min_expiration) * random.random()).strftime('%Y-%m-%d')

    validity = {
        'Version': version,
        'Expiration_Date': expiration_date
        }

    return validity

# Return 1 Doctor - (0,5) Nurses
def getMedicalTeam() -> (list, list):

    doctor = dict()
    nurses = list()
    CIF = ""
    
    while CIF == "":
        sex = random.choice(['male','female'])
        first_name = names.get_first_name(gender=sex)
        last_name = names.get_last_name()
        birth = (birth_min_datetime + (birth_max_datetime - birth_min_datetime) * random.random()).strftime('%Y-%m-%d')
        birthplace = cities[random.randint(0,len(cities))]

        try:
            CIF = codicefiscale.encode(surname=last_name, name=first_name, sex=sex[0].upper(), birthdate=birth, birthplace=birthplace)
        except:
            print('Codicefiscale broken')
            continue

    doctor = {
        '_id': CIF,
        'First_Name': first_name,
        'Last_Name': last_name
        }

    for i in range(random.randint(max_nurses)):
        sex = random.choice(['male','female'])
        first_name = names.get_first_name(gender=sex)
        last_name = names.get_last_name()
        birth = (birth_min_datetime + (birth_max_datetime - birth_min_datetime) * random.random()).strftime('%Y-%m-%d')
        birthplace = cities[random.randint(0,len(cities))]

        try:
            CIF = codicefiscale.encode(surname=last_name, name=first_name, sex=sex[0].upper(), birthdate=birth, birthplace=birthplace)
        except:
            print('Codicefiscale broken')
            continue

        nurses.append({
            '_id': CIF,
            'First_Name': first_name,
            'Last_Name': last_name
            })

    return doctor, nurses

# Simple Emergency Contacts  generator
def getEmergencyContact() -> list:

    mail_provider  = random.choice(['gmail.com','outlook.it','icloud.com','hotmail.it','yahoo.it'])
    email = f'{names.get_first_name().lower()}.{names.get_last_name().lower()}@{mail_provider}'

    emergency_contact = {
        'e_mail': email,
        'Description': 'This is a sample Description!'
    }

    return emergency_contact


# Return Documents
def getDocuments() -> (list):

    certificates = list()

    for i in range(NUMBER_OF_CERTIFICATES):

        tests = list()
        vaccines = list()

        sex = random.choice(['male','female'])
        first_name = names.get_first_name(gender=sex)
        last_name = names.get_last_name()
        birth = (birth_min_datetime + (birth_max_datetime - birth_min_datetime) * random.random()).strftime('%Y-%m-%d')
        birthplace = cities[random.randint(0,len(cities))]

        try:
            CIF = codicefiscale.encode(surname=last_name, name=first_name, sex=sex[0].upper(), birthdate=birth, birthplace=birthplace)
        except:
            print('Codicefiscale broken')
            continue

        validity = getValidity()
        emergency_contact = getEmergencyContact()

        
        # Discrete ~Normal Distribution~ centered in 0 for number of test per person
        x = arange(0, max_tests)
        xU, xL = x + 0.5, x - 0.5 
        prob = ss.norm.cdf(xU, scale = 3) - ss.norm.cdf(xL, scale = 3)
        prob = prob / prob.sum() 
        num = random.choice(x, p=prob)

        for i in range(num):

            doctor, nurses = getMedicalTeam()
            tests.append({
                'CIF': CIF,
                'Date': (min_datetime + (max_datetime - min_datetime) * random.random()).strftime('%Y-%m-%d'),
                'Result': bool(random.choice([True,False], p=[positive_ratio, 1 - positive_ratio])),
                'Place_ID': random.randint(num_places),
                'Doctor': doctor,
                'Nurses': nurses
            })


        for i in range(random.randint(max_vaccines)):

            doctor, nurses = getMedicalTeam()
            date = (min_datetime + (max_datetime - min_datetime) * random.random())
            vaccines.append({
                'CIF': CIF,
                'Date': date.strftime('%Y-%m-%d'),
                'Brand': random.choice(["Pfizer", "Moderna", "Astrazeneca", "Johnson & Johnson"]),
                'Place_ID': random.randint(num_places),
                'Type': random.choice(['mRNA', 'Viral Vector']),
                'Production_Date': (min_datetime + (date - min_datetime) * random.random()).strftime('%Y-%m-%d'),
                'Doctor': doctor,
                'Nurses': nurses
            })


        # Sorting by Date
        vaccines = sorted(vaccines, key=lambda x: x['Date'])
        tests = sorted(tests, key=lambda x: x['Date'])

        # If no vaccine but tests
        if(not (len(vaccines))):
            if(len(tests)):
                validity['Expiration_Date'] = ((datetime.strptime(tests[-1]['Date'], '%Y-%m-%d')) + relativedelta(hours=48)).strftime('%Y-%m-%d')
            else:
                validity = None

        certificates.append({
            '_id': CIF,
            'First_Name': first_name,
            'Last_Name': last_name,
            'Birth': birth,
            'Birthplace': birthplace,
            'Validity': validity,
            'Emergency_Contact': emergency_contact,
            'Tests': tests,
            'Vaccines': vaccines
            })


    return certificates, 

if __name__ == '__main__':

    # Get Documents
    certificates = getDocuments()

    # Exports Collections
    saveJSON(certificates[0], "./output/certificates.json")
    saveJSON(json.loads(places_df.to_json(orient='records')),'./output/places.json')




