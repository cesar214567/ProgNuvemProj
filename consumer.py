import threading, time
from tokenize import group
import json
from kafka import KafkaAdminClient, KafkaConsumer, KafkaProducer
from kafka.admin import NewTopic
from filters import filter_file, getLanguage
#from model import entities,db,engine
from model.entities import *
from database import connector
from datetime import datetime

class Consumer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        consumer = KafkaConsumer('my-topic',
                                 bootstrap_servers='localhost:9092',
                                 group_id =None,
                                 auto_offset_reset='earliest',
                                 consumer_timeout_ms=1000,api_version=(0,10))

        while not self.stop_event.is_set():
            for message in consumer:
                temp = json.loads(message.value)
                temp = json.loads(temp)['text']
                data = getLanguage(temp)
                if data['language']=='es' and data['score'] > 0.95:
                    tweets = filter_file(temp)
                    for tweet in tweets:
                        session = db.getSession(engine)
                        object = Tweet(
                            text = tweet,
                            date = datetime.now()
                        )
                        session.add(object)
                        session.commit()
                        session.close()
                        print(object)
                if self.stop_event.is_set():
                    break

        consumer.close()


def main():
    # Create 'my-topic' Kafka topic
    try:
        admin = KafkaAdminClient(bootstrap_servers='localhost:9092',api_version=(0,10))

        topic = NewTopic(name='my-topic',
                         num_partitions=1,
                         replication_factor=1)
        admin.create_topics([topic])
    except Exception:
        pass

    task = Consumer()

    # Start threads of a publisher/producer and a subscriber/consumer to 'my-topic' Kafka topic
    task.start()

    time.sleep(100)

    # Stop threads
    task.stop()

    task.join()


if __name__ == "__main__":
    main()