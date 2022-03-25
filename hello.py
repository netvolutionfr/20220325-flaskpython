from flask import Flask, make_response
from flask_pymongo import PyMongo
import json, bson
from datetime import date, datetime
from flask_cors import CORS, cross_origin

def json_response(obj, cls=None):
    response = make_response(json.dumps(obj, cls=cls))
    response.content_type = 'application/json'

    return response

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, bson.ObjectId):
            return str(o)
        if isinstance(o, (datetime, date)):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/new_york'
mongodb_client = PyMongo(app)
db = mongodb_client.db

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

@app.route('/restaurants', methods=['GET'])
@cross_origin()
def restaurants(cuisine="Mexican"):
    restaurants = db.restaurants.find({"borough": "Brooklyn", "cuisine": cuisine, "address.street": "5 Avenue"})
    return json_response({'restaurants': [r for r in restaurants]}, cls=JSONEncoder)
