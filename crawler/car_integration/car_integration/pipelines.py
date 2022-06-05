# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import logging
import sys

# useful for handling different item types with a single interface
import pymongo
from pymongo.errors import ConnectionFailure
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings
from confluent_kafka import Producer
import json
import time

settings = get_project_settings()


def connect_database():
    try:
        connection = pymongo.MongoClient(
            settings['MONGODB_URI']
        )
        return connection[settings['MONGODB_DB']]
    except ConnectionFailure as e:
        print("Error when try to connect mongodb: %s" % e)
        sys.exit()

class MongoDBPipeline(object):
    
    def __init__(self):
        db = connect_database()
        self.count = 0
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))

        if valid:
            try:
                filter_link = {'source': item.get('source')}
                if self.collection.find(filter_link).count() > 0:
                    self.collection.replace_one(filter_link, item, upsert=True)
                else:
                    self.collection.insert(dict(item))
            except Exception as e:
                logging.error("An exception occurred :" + e)
                return False

            self.count += 1

            if self.count % 100 == 0:
                logging.info("Added " + str(self.count) + " records from " + spider.name + " into MongoDB database!")

        return item
    
class KafkaPipeline(object):
    
    def __init__(self):
        self.bootstrap_servers = "localhost:29092"
        self.topic = "data_log"
        self.p = Producer({'bootstrap.servers': self.bootstrap_servers})

    def produce(self, msg):
    
        serialized_message = json.dumps(msg)
        self.p.produce(serialized_message)
        self.p.poll(0)
        time.sleep(1)
        # self.p.flush()

class CarIntegrationPipeline:
    def process_item(self, item, spider):
        return item
