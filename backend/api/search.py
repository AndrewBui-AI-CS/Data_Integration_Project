import json
import time

import flask
from backend import api, constants, mongodb
from backend.api import JSONEncoder
from flask import request


def find():
    print("Searching!")
    text = request.args.get('text')
    mfg = request.args.get('mfg')
    manufacturer = request.args.get('manufacturer')
    seat = request.args.get('seat')
    price_min = request.args.get('min-price')
    price_max = request.args.get('max-price')
    page = request.args.get('page')
    type_product = request.args.get('type')

    query = {}
    if text or mfg or manufacturer or seat or price_max or price_min or type_product:
        query_children = {'bool': {'must': [], 'should': []}}
        if text is not None:
            query_children['bool']['must'].append({'match': {'name': text}})

        if manufacturer is not None:
            query_children['bool']['must'].append({'match': {'manufacturer': manufacturer}})

        if type_product is not None:
            query_children['bool']['must'].append({'match': {'type': type_product}})

        if (price_max is not None and price_min is not None) or mfg is not None:
            dict_range = {}
            if price_max is not None or price_min is not None:
                if price_max is None:
                    price_max = 100000000000
                if price_min is None:
                    price_min = 0
                query_children['bool']['must'].append({'range': {'price': {
                    'gte': price_min,
                    'lte': price_max,
                }}})

            if mfg is not None:
                dict_range['mfg'] = {
                    'gte': mfg,
                }
                query_children['bool']['must'].append({'range': {'mfg': {
                    'gte': mfg,
                }}})

        if seat is not None:
            dict_term = {'seat': seat}
            query_children['bool']['must'].append({'term': dict_term})

        query = {'query': query_children}

    count = api.count_record(query)

    if page is not None:
        query['from'] = int(page) * (constants.SIZE_PAGE - 1)

    start = time.time()
    cars = api.query_db(query, size=constants.SIZE_PAGE)
    total_time = time.time() - start
    return {'time request': f'{total_time} s ', 'total': count, 'data': cars}


def get_list_manufacturer():
    list_manufacturer = mongodb.config.find_one()
    return flask.jsonify({'data': json.loads(JSONEncoder(ensure_ascii=False).encode(list_manufacturer))})
