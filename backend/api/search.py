import flask
import json

from backend.api.car_filter import CarFilter
from flask import request
from bson import json_util


car_filter = CarFilter()

def create_app():
    app = flask.Flask(__name__)
    
    @app.route("/")
    def index():
        return "Hello World!"
    
    #  =====================      ARTICLE   APIs      =====================  #
    
    @app.route("/filter")
    def get_filter_result():
        car_cursor = car_filter.car_db.find({'price': { "$gt": 3699000000 }})
        fields = car_cursor[0].keys()
        request_fields = {field: request.args.get(field) for field in fields}
        request_fields['price_sort']  = request.args.get('price_sort')
        request_fields['seat_sort']  = request.args.get('seat_sort')
        request_fields['mfg_sort']  = request.args.get('mfg_sort')
        # request.args["deviceid"] if "deviceid" in request.args else None
        query = {}
        for key, value in request_fields.items():
            if key == 'price':
                if request_fields['price_sort'] == 'gt':
                    query[key] = {'$gt': int(value)}
                    continue
                elif request_fields['price_sort'] == 'lt':
                    query[key] = {'$lt': int(value)}
                    continue
                    
            if key == 'seat':
                if request_fields['seat_sort'] == 'gt':
                    query[key] = {'$gt': int(value)}
                    continue
                elif request_fields['seat_sort'] == 'lt':
                    query[key] = {'$lt': int(value)}
                    continue
                    
            if key == 'mfg':
                if request_fields['mfg_sort'] == 'gt':
                    query[key] = {'$gt': int(value)}
                    continue
                elif request_fields['mfg_sort'] == 'lt':
                    query[key] = {'$lt': int(value)}
                    continue
    
            if key in ['price_sort', 'seat_sort', 'mfg_sort']:
                continue
            
            if value is not None:
                if value in ['price', 'seat', 'mfg']:
                    query[str(key)] = int(value)
                else:
                    query[str(key)] = value
                    
        for key, value in query.items():
            if type(value) is dict:
                continue
            if value.isnumeric():
                query[key] = int(value)
        car_cursor = list(car_filter.car_db.find(query))
        result = get_result_format(car_cursor)
        return result
    
    def parse_json(data):
        return json.loads(json_util.dumps(data))
    
    def get_result_format(rec_list):
        result = dict()
        d = []
        for item_id in rec_list:
            d.append(parse_json(item_id))
        result["result"] = d
        return result
    
    return app