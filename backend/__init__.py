import pymongo
from crawler.car_integration.car_integration import settings
from elasticsearch import Elasticsearch
from flask import Flask
from flask_cors import CORS

import constants

mongodb = pymongo.MongoClient(
    settings.MONGODB_SERVER,
    settings.MONGODB_PORT
)[settings.MONGODB_DB]

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False
CORS(app)

# es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
es = Elasticsearch("http://localhost:9200")
es.indices.put_settings(index=constants.ELASTICSEARCH_INDEX,
                        body={"index": {
                            "max_result_window": 500000
                        }})
