import json
from random import randrange

import flask
from backend import api, constants, mongodb
from backend.api import JSONEncoder
from bson.objectid import ObjectId
from crawler.car_integration.car_integration import settings


def get_list_data_matching(model: str, type_product: str):
    query = {
        'query': {
            "bool": {
                'must': [
                    {
                        'match': {
                            'model': model,
                        }
                    },
                    {
                        'match': {
                            'type': type_product,
                        }
                    }
                ]
            }
        }
    }
    return api.query_db(query, size=constants.NUMBER_DATA_MATCHING)


def get_list_product_same_source(source: str):
    query = {
        'query': {
            'bool': {
                'must': {
                    'match': {
                        'base_url': source
                    }
                }
            }
        },
        'from': randrange(80000)
    }
    return api.query_db(query, size=constants.NUMBER_PRODUCT_SAME_SOURCE)


def detail_product(id_product: str):
    detail = mongodb[settings.MONGODB_COLLECTION].find_one({"_id": ObjectId(id_product)})
    try:
        list_data_matching = get_list_data_matching(detail['model'], detail['type'])
    except Exception as e:
        list_data_matching = None

    try:
        list_product_same_source = get_list_product_same_source(detail['base_url'])
    except Exception as e:
        print(e)
        list_product_same_source = None

    return flask.jsonify({
        'data': json.loads(JSONEncoder(ensure_ascii=False).encode(detail)),
        'list_data_matching': list_data_matching,
        'list_product_same_source': list_product_same_source,
    })


def get_list_same_price(price: int):
    query = {
        'query':
            {
                'range': {
                    'price': {
                        'gte': price - constants.RANGE_PRICE_RELATED,
                        'lte': price + constants.RANGE_PRICE_RELATED,
                    }
                }
            }
    }

    cars = api.query_db(query, size=constants.NUMBER_SAME_PRICE_PRODUCT_RELATED)
    return {'total': len(cars), 'data': cars}


def get_list_same_manufacturer(manufacturer: str):
    query = {
        'query': {
            'match': {
                'manufacturer': manufacturer,
            }
        }
    }

    cars = api.query_db(query, size=constants.NUMBER_SAME_MANUFACTURER_PRODUCT_RELATED)
    return {'total': len(cars), 'data': cars}
