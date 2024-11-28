"""Produce openweathermap content to 'weather' kafka topic."""
from faker import Faker
import asyncio
import configparser
import os
import time
from collections import namedtuple
from kafka import KafkaProducer
import json

from geopy.geocoders import Nominatim
import requests
import json
import numpy as np

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
TOPIC_NAME = os.environ.get("TOPIC_NAME", "air_quality")
SLEEP_TIME = int(os.environ.get("SLEEP_TIME", 60))


fake = Faker()


def get_registered_user():
    return {
        "name": fake.name(),
        "address": fake.address(),
        # "year": fake.year()
    }


def get_air_quality(city: str, iterator):
    geolocator = Nominatim(user_agent="nothing yet")

    location = geolocator.geocode(city)
    print((location.latitude, location.longitude))

    url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={location.latitude}&longitude={location.longitude}&hourly=pm10,pm2_5&forecast_days=1"

    response = requests.get(url)
    response = response.json()

    # return {
    #     'location': city,
    #     'date': response['hourly']['time'][0][:10],
    #     'pm10': np.mean(response['hourly']['pm10']),
    #     'pm2_5': np.mean(response['hourly']['pm2_5'])
    # }
    return {
        'ind': str(iterator),
        'location': city,
        'forcastdate': str(response['hourly']['time'][0][:10]),
        'pm10': round(np.mean(response['hourly']['pm10']), 2),
        'pm2_5': round(np.mean(response['hourly']['pm2_5']), 2)
    }


def run():
    cities = ['Ho Chi Minh', 'Dubai', 'San Diego', 'Cape Town', 'Mumbai', 'Vancouver']
    iterator = 0
    print("Setting up Faker producer at {}".format(KAFKA_BROKER_URL))
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER_URL],
        # Encode all values as JSON
        value_serializer=lambda x: json.dumps(x).encode('utf-8'),
    )

    while True:
        city = cities[(iterator + 1) % len(cities)]
        sendit = get_air_quality(city, iterator)
        # adding prints for debugging in logs
        print("Sending new faker data iteration - {}".format(iterator))
        # sendit = get_registered_user()
        print('here is send it')
        print(sendit)
        producer.send('air_quality', value=sendit)
        print("New air quality data sent")
        time.sleep(SLEEP_TIME)
        print("Waking up!")
        iterator += 1


if __name__ == "__main__":
    run()
