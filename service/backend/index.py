from flask import Flask, make_response, request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from
#from flask_cors import CORS
import random
import json
import db

app = Flask(__name__)
app.json_encoder = LazyJSONEncoder
#CORS(app)


swagger_template = dict(
info = {
    'title': LazyString(lambda: 'Backend API'),
    'version': LazyString(lambda: '0.1'),
    'description': LazyString(lambda: 'This document describe how to interact with the Backend'),
    },
    host = LazyString(lambda: request.host)
)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'hello_world',
            "route": "/hello_world.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

PORT = 3001
HOST = '0.0.0.0'

data_activities = []
data_restaurants = []

hist_activities = []
hist_restaurants = []

swagger = Swagger(app, template=swagger_template,             
                  config=swagger_config)



def load_data():
    global data_activities
    global data_restaurants
    with open('dummy.json', 'r') as activity_file:
        data_activities = json.load(activity_file)
    with open('dummy_restaurant.json', 'r') as restaurant_file:
        data_restaurants = json.load(restaurant_file)


def load_data_from_db():
    db.db_connect()
    global data_activities
    global data_restaurants
    data_activities = db.send_request('''SELECT * FROM Activity''')
    data_restaurants = db.send_request('''SELECT * FROM Restaurant''')

def random_selection(mid_day, data, hist):
    """
    Perform random selection of activity available at that time.

    :param mid_day: integer, an integer representing a half of a day, ranging from 0 to 13
    :param data: list of dict, the data in which perform the random selection
    :param hist: list of dict, the history of previously selected elements
    :return: a dict corresponding to the activity chosen
    """
    assert type(mid_day) is int, "Received wrong type"
    choices = []
    for element in data:
        if element["opened"][mid_day]:
            choices.append(element)

    while len(choices) > 0:
        rand_id = random.randint(0, len(choices)-1)
        result = choices.pop(rand_id)
        if result["recordid"] not in hist:
            hist.append(result["recordid"])
            res = {
            "name" : result["fields"]["nom_complet"],
            "adress" : result["fields"]["adresse"],
            "type" : result["fields"]["type"]
        }
            return res

    return "bof"


def basic_agenda(day):
    """
    Create a basic agenda consisting of randomly selected activities and restaurant for
    the first half and second half of the day and for lunch and dinner.
    :param day: int, ranging from 0 to 6, the day for which the function aims at creating an agenda
    :return: list of dict, list of elements consisting of activities and restaurants, ordered by
    appearance in the day.
    """

    assert type(day) is int, "Received wrong type"

    day_agenda = []

    fst_half = 2*day
    scd_half = 2*day+1
    day_agenda.append(random_selection(fst_half, data_activities, hist_activities))
    day_agenda.append(random_selection(fst_half, data_restaurants, hist_restaurants))
    day_agenda.append(random_selection(scd_half, data_activities, hist_activities))
    day_agenda.append(random_selection(scd_half, data_restaurants, hist_restaurants))

    return day_agenda


@swag_from("./docs/swagger_home.yml", methods=['GET'])
@app.route("/", methods=['GET'])
def home():
    res = {
        "bonjour": "bonjour"
    }
    return make_response(res, 200)


@swag_from("./docs/swagger_activity.yml")
@app.route("/activity", methods=['GET'])
def get_activity():
    time = int(request.args.get('time'))
    activity = random_selection(time, data_activities, hist_activities)
    if activity == "bof":
        result = {"error": "no more activity not already seen"}
        return make_response(result,400)
    else:
        return make_response(activity,200)


@swag_from("./docs/swagger_restaurant.yml")
@app.route("/restaurant", methods=['GET'])
def get_restaurant():
    time = int(request.args.get('time'))
    restaurant = random_selection(time, data_restaurants, hist_restaurants)
    if restaurant == "bof":
        result = {"error":"no more restaurant not already seen"}
        return make_response(result, 400)
    else:
        return make_response(restaurant, 200)

###
# TO UPDATE
### 
@swag_from("./docs/swagger_agenda.yml")
@app.route("/agenda", methods=['GET'])
def get_agenda():
    time = int(request.args.get('time'))
    agenda = basic_agenda(time)
    if "bof" in agenda:
        return make_response(agenda, 300)
    else:
        return make_response(agenda,200)

if __name__ == "__main__":
    load_data()
    print(basic_agenda(0))
    app.run(host=HOST, port=PORT)
