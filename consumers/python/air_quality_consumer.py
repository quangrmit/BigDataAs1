from kafka import KafkaConsumer
import os, json


if __name__ == "__main__":
    print("Starting Air Quality Consumer")
    TOPIC_NAME = os.environ.get("AIR_QUALITY_TOPIC_NAME", "air_quality")
    KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL", "localhost:9092")
    CASSANDRA_HOST = os.environ.get("CASSANDRA_HOST", "localhost")
    CASSANDRA_KEYSPACE = os.environ.get("CASSANDRA_KEYSPACE", "kafkapipeline")

    print("Setting up Kafka consumer at {}".format(KAFKA_BROKER_URL))
    consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=[KAFKA_BROKER_URL])
    
    print('Waiting for msg...')
    for msg in consumer:
        msg = msg.value.decode('utf-8')
        jsonData=json.loads(msg)
        # add print for checking
        print(jsonData)
  