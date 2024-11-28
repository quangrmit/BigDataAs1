"""Produce openweathermap content to 'weather' kafka topic."""
import asyncio
import configparser
import os
import time
from collections import namedtuple
from kafka import KafkaProducer
import json

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
TOPIC_NAME = os.environ.get("TOPIC_NAME")
SLEEP_TIME = int(os.environ.get("SLEEP_TIME", 60))

from faker import Faker

fake = Faker()

def get_registered_user():
    return {
        "name": fake.name(),
        "address": fake.address(),
        "year": fake.year(),
        "bank": fake.aba(),
        "favourite_color": fake.color(),
        "credit_card": fake.credit_card_expire(),
        "company_email": fake.company_email(),
        "domain_name": fake.domain_name(),
        "avatar" : fake.image_url(),
        "job" : fake.job()
    }


def run():
    iterator = 0
    print("Setting up Faker producer at {}".format(KAFKA_BROKER_URL))
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER_URL],
        # Encode all values as JSON
        value_serializer=lambda x: json.dumps(x).encode('utf-8'),
    )

    while True:
        sendit = get_registered_user()
        # adding prints for debugging in logs
        print("Sending new faker data iteration - {}".format(iterator))
        producer.send(TOPIC_NAME, value=sendit)
        print("New faker data sent")
        time.sleep(SLEEP_TIME)
        print("Waking up!")
        iterator += 1

if __name__ == "__main__":
    run()
