from elasticsearch7 import Elasticsearch
import time
from datetime import datetime
import glob
import json



class Elastic:

    def __init__(self,
                 host = "localhost",
                 port = 9200,
                 es = None,
                 index = "car"):
        self.host = host
        self.port = port
        self.es = es
        self.connect()
        self.index = index
        
    def connect(self):
        self.es = Elasticsearch([{'host': self.host, 'port': self.port}])
        if self.es.ping():
            print("ES connected successfully")
        else:
            print("Not connected")

    def create_index(self):
        if self.es.indices.exists(self.index):
            print("deleting '%s' index..." % (self.index))
            res = self.es.indices.delete(index=self.index)
            print(" response: '%s'" % (res))
    #         request_body = {
    #         "settings": {
    #             "analysis": {
    #             "filter": {
    #                 "autocomplete_filter": {
    #                     "type": "edge_ngram",
    #                     "min_gram": 1,
    #                     "max_gram": 20
    #                 }
    #             },
    #         "analyzer": {
    #                 "autocomplete": { 
    #                     "type": "custom",
    #                     "tokenizer": "standard",
    #                     "filter": [
    #                         "lowercase",
    #                         "autocomplete_filter"
    #                     ]
    #                 }
    #             }
    #         }
    #     },
    #     "mappings": {
    #         "properties": {
    #             "text": {
    #                 "type": "text",
    #                 "analyzer": "autocomplete", 
    #                 "search_analyzer": "standard" 
    #             }
    #         }
    #     }
    # }
            print("creating '%s' index..." % (self.index))
            res = self.es.indices.create(index=self.index, ignore=400)
            print(" response: '%s'" % (res))

    def push_to_index(self, message):
        try:
            response = self.es.index(
                index=self.index,
                doc_type="log",
                body=message
            )
            print("Write response is :: {}\n\n".format(response))
        except Exception as e:
            print("Exception is :: {}".format(str(e)))




if __name__ == '__main__':
    es_obj = Elastic()
    es_obj.create_index()
    with open("car.json","r") as f:
        data = [json.loads(record) for record in f.readlines()]
        removed_fields = ['_id', 'time_update', 'image']
        es_data =[{k:v for k,v in record.items() if k not in removed_fields} for record in data]
        for record in es_data:
            es_obj.push_to_index(record)