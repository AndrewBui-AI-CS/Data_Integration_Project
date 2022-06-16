# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import logging
import sys

# useful for handling different item types with a single interface
import pymongo
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo.errors import ConnectionFailure
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings

settings = get_project_settings()


def connect_database():
    try:
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
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
                print(filter_link)
                print(self.collection.find(filter_link))
                # if self.collection.find(filter_link).count() > 0:
                #     self.collection.replace_one(filter_link, item, upsert=True)
                # else:
                self.collection.insert_one(dict(item))
            except Exception as e:
                print("An exception occurred :", e)
                return False

            # self.count += 1

            # if self.count % 100 == 0:
            #     logging.info("Added " + str(self.count) + " records from " + spider.name + " into MongoDB database!")

        return item

# class CarIntegrationPipeline:
#     def process_item(self, item, spider):
#         return item

class DefaultValuesPipeline(object):
    @staticmethod
    def process_item(item, spider):
        item.setdefault('overall_dimension', '')
        item.setdefault('cylinder_capacity', '')
        item.setdefault('engine', '')
        item.setdefault('max_wattage', '')
        item.setdefault('fuel_consumption', '')
        item.setdefault('origin', '')
        item.setdefault('transmission', '')
        item.setdefault('manufacturer', '')
        item.setdefault('type', '')
        item.setdefault('color', '')
        item.setdefault('interior_color', '')
        item.setdefault('mfg', '')
        item.setdefault('drive', '')
        item.setdefault('fuel_tank_capacity', '')
        item.setdefault('status', '')
        return item
