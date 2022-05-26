import tweepy
import csv
import pandas as pd

from kafka import KafkaProducer
from json import dumps
import json
import os

access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         api_version=(0, 11, 5),
                         value_serializer=lambda x: dumps(x).encode('utf-8'))


class IDPrinter(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        print(tweet.data)
        print(type(tweet.data))
        producer.send("my-topic", json.dumps(tweet.data))


printer = IDPrinter(bearer_token=os.getenv("BEARER_TOKEN"))
print(printer.get_rules())
printer.filter()
