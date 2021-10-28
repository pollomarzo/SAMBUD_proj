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
        'last_confirm': min_datetime + (max_datetime - min_datetime) * random.random(),
    }) for i in range(SIZE_DATASET)
]


print(people)
