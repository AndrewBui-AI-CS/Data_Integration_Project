import pymongo
from crawler.car_integration.car_integration import settings

mongodb = pymongo.MongoClient(
    settings.MONGODB_URI
)[settings.MONGODB_DB]