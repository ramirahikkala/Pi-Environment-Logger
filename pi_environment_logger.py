import time
import os
from pymongo import MongoClient
import Adafruit_BMP.BMP085 as BMP085
from datetime import datetime

FREQUENCY_SECONDS = 30


def main():
    client = MongoClient(
        'mongodb+srv://'
        + os.environ['KOTI_CONNECTION_USER']
        + ':'
        + os.environ['KOTI_CONNECTION_PWD']
        + '@'
        + os.environ['KOTI_CONNECTION']
        + '/?retryWrites=true&w=majority'
    )

    db = client.koti
    bmp = BMP085.BMP085()
    previous = None

    while True:
        environment = {
            'temp': bmp.read_temperature(),
            'pressure': bmp.read_pressure(),
            'date': datetime.now(),
            'location': os.environ['KOTI_LOCATION'],
        }
        if environment != previous:
            db.environment.insert_one(environment)
            previous = environment
        time.sleep(FREQUENCY_SECONDS)


main()
