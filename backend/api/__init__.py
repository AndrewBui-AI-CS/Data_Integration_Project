import json

from bson.objectid import ObjectId

from backend import es
from backend.constants import ELASTICSEARCH_INDEX
from datetime import datetime


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, datetime):
            return o.strftime("%m/%d/%Y, %H:%M:%S")

        return json.JSONEncoder.default(self, o)


def get_item(hits):
    result = []
    for item in hits:
        item['_source']['id'] = item['_id']
        result.append(item['_source'])
    return result


def query_db(query: dict, size: int):
    res = es.search(index=ELASTICSEARCH_INDEX, size=size, body=query)
    return get_item(res['hits']['hits'])


def count_record(query: dict):
    res = es.count(index=ELASTICSEARCH_INDEX, body=query)
    return res['count']
