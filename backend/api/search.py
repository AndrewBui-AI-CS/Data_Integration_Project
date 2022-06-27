import flask
import pymongo
from backend import mongodb
from backend.api.car_filter import CarFilter
from flask import request

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
        # request.args["deviceid"] if "deviceid" in request.args else None
        print(request_fields)
    return app