import names
import random

from datetime import datetime, timedelta


SIZE_DATASET = 10

min_datetime = datetime(2018, 1, 1, 0, 0, 0)
max_datetime = datetime.now()

people = [
    ({
        'code': i,
        'first_name': names.get_first_name(),
        'last_name': names.get_last_name(),
        'positive': random.choice([True, False]),
        # brith, phone_number, email
        'birth': '01/01/1990',
        'phone_number': '000',
        'email': 'mail@example.com',
        'last_confirm': random.choice([None, min_datetime + (max_datetime - min_datetime) * random.random()]),
    }) for i in range(SIZE_DATASET)
]

medical_records = [
    ({
        'code': i,
        'covid_vaccinated': random.choice([True, False]),
        'risky_subject': random.choice([True, False]),
        'health_status': random.choice(["bad", "average", "good"]),
    }) for i in range(SIZE_DATASET)
]

medical_vaccines = []

for i in medical_records:
    if (i.covid_vaccinated):
        medical_vaccines.append({
            'code': i.code,
            'date': min_datetime + (max_datetime - min_datetime) * random.random(),
            'type': random.choice(["pfizer", "moderna", "astrazeneca"])
        })

covid_tests = []
for i in people:
    if (i.last_confirm != None):
        covid_tests.append({
            'code': i.code,
            'date': i.last_confirm,
            'result': i.positive,
        })


print(people)
