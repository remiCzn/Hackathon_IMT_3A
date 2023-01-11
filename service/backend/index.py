from flask import Flask, make_response, request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from
#from flask_cors import CORS
import numpy as np
import random
import jwt as jwt
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

#hist_activities = []
#hist_restaurants = []

tag_list = ["Médiathèque", "Salle de spectacle", "Monument", "Musée, Chateau", "Ecole Culturelle", "Salle d'exposition", "Cinéma"]

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
    data_activities = json.loads(db.send_request('''SELECT * FROM Activity'''))
    data_restaurants = json.loads(db.send_request('''SELECT * FROM Restaurant'''))

def preprocessing(data):
    for element in data:
        element["schedule"] = [1 for i in range(14)] if (element["schedule"] == 'NA')\
                                                    else [int(c) for c in list(element["schedule"])]
        element["schedule"] = [int(c) for c in list(element["schedule"])]
        element["coordinate"] = [float(n) for n in element["coordinate"].split(",")]
    return data

def decode(token):
    return jwt.decode(token, "secret", algorithms=["HS256"])

def encode(label, token):
    assert type(label) is str, "label should be a string"
    
    return jwt.encode({label: token}, "secret", algorithm="HS256")

def get_tag_list():

    _tag_list = []
    for element in data_activities:
        if element["category"] not in _tag_list : _tag_list.append(element["category"])
    for element in data_restaurants:
        if element["category"] not in _tag_list : _tag_list.append(element["category"])

    return _tag_list


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
        if element["schedule"][mid_day]:
            choices.append(element)

    while len(choices) > 0:
        rand_id = random.randint(0, len(choices)-1)
        result = choices.pop(rand_id)
        if result["activityid"] not in hist:
            hist.append(result["activityid"])
            res = {
            "name" : result["name"],
            "adress" : result["address"],
            "categorie" : result["category"]
        }
            return res, hist

    return "bof", hist


def selection_by_distance(mid_day, pos, r, data, hist):
    """
    Perform random selection of activity available at that time based on the distance to the user.

    :param mid_day: integer, an integer representing a half of a day, ranging from 0 to 13
    :param pos: tuple(float, float), a tuple containing the latitude and the longitude of the user such that pos = (lat, long)
    :param r: int, the max distance from the user to the point of interest in km
    :param data: list of dict, the data in which perform the random selection
    :param hist: list of dict, the history of previously selected elements
    :return: a dict corresponding to the activity chosen
    """

    assert type(mid_day) is int, "Received wrong type"
    choices = []
    for element in data:
        if element["schedule"][mid_day]:
            dist = get_distance(pos[0], pos[1], element["coordinate"][0], element["coordinate"][1])
            if dist <= r:
                choices.append(element)
    
    while len(choices) > 0:
        rand_id = random.randint(0, len(choices)-1)
        result = choices.pop(rand_id)
        if result["activityid"] not in hist:
            hist.append(result["activityid"])
            res = {
            "name" : result["name"],
            "adress" : result["address"],
            "categorie" : result["category"]
        }
            return res, hist

    return "bof", hist


def selection_by_tags_distance(mid_day, pos, r, tags, data, hist):
    """
    Perform random selection of activity available at that time based on the distance
    to the user and the tags provided.

    :param mid_day: integer, an integer representing a half of a day, ranging from 0 to 13
    :param pos: tuple(float, float), a tuple containing the latitude and the longitude of the user such that pos = (lat, long)
    :param r: int, the max distance from the user to the point of interest in km
    :param tags: list[string], the list of tags to which the user want the activity to belong to
    :param data: list of dict, the data in which perform the random selection
    :param hist: list of dict, the history of previously selected elements
    :return: a dict corresponding to the activity chosen
    
    """

    assert type(mid_day) is int, "Received wrong type"
    assert type(tags) is list, "tags should be a list"

    choices = []
    for element in data:
        if element["schedule"][mid_day]:
            dist = get_distance(pos[0], pos[1], element["coordinate"][0], element["coordinate"][1])
            if (dist <= r) & (element["category"] in tags):
                choices.append(element)

    while len(choices) > 0:
        rand_id = random.randint(0, len(choices)-1)
        result = choices.pop(rand_id)
        if result["activityid"] not in hist:
            hist.append(result["activityid"])
            res = {
            "name" : result["name"],
            "adress" : result["address"],
            "categorie" : result["category"]
        }
            return res, hist

    return "bof", hist


def basic_agenda(day, hist):
    """
    Create a basic agenda consisting of randomly selected activities and restaurant for
    the first half and second half of the day and for lunch and dinner.
    :param day: int, ranging from 0 to 6, the day for which the function aims at creating an agenda
    :param hist: list of dict, the history of previously selected elements
    :return: list of dict, list of elements consisting of activities and restaurants, ordered by
    appearance in the day.
    """

    assert type(day) is int, "Received wrong type"

    day_agenda = []

    fst_half = 2*day
    scd_half = 2*day+1

    activity1, hist = random_selection(fst_half, data_activities, hist)
    day_agenda.append(activity1)

    restaurant1, hist = random_selection(fst_half, data_restaurants, hist)
    day_agenda.append(restaurant1)

    activity2, hist = random_selection(scd_half, data_activities, hist)
    day_agenda.append(activity2)

    restaurant2, hist = random_selection(scd_half, data_restaurants, hist)
    day_agenda.append(restaurant2)

    return day_agenda, hist 


def by_distance_agenda(day, pos, r, hist):
    """
    Create an agenda respecting a distance criterion consisting of randomly
    selected activities and restaurant for the first half and second half of the day and 
    for lunch and dinner.
    :param day: int, ranging from 0 to 6, the day for which the function aims at creating an agenda
    :param pos: tuple(float, float), a tuple containing the latitude and the longitude of the user such that pos = (lat, long)
    :param r:  int, the max distance from the user to the point of interest in km
    :param hist: list of dict, the history of previously selected elements
    :return: list of dict, list of elements consisting of activities and restaurants, ordered by
    appearance in the day.
    """

    assert type(day) is int, "Received wrong type"

    day_agenda = []

    fst_half = 2*day
    scd_half = 2*day+1

    activity1, hist = selection_by_distance(fst_half, pos, r, data_activities, hist)
    day_agenda.append(activity1)

    restaurant1, hist = selection_by_distance(fst_half, pos, r, data_restaurants, hist)
    day_agenda.append(restaurant1)

    activity2, hist = selection_by_distance(scd_half, pos, r, data_activities, hist)
    day_agenda.append(activity2)

    restaurant2, hist = selection_by_distance(scd_half, pos, r, data_restaurants, hist)
    day_agenda.append(restaurant2)

    return day_agenda, hist


def by_tags_distance_agenda(day, pos, r, tags, hist):
    """
    Create an agenda respecting a distance criterion and tags criteria, consisting of randomly
    selected activities and restaurant for the first half and second half of the day and 
    for lunch and dinner.
    :param day: int, ranging from 0 to 6, the day for which the function aims at creating an agenda
    :param pos: tuple(float, float), a tuple containing the latitude and the longitude of the user such that pos = (lat, long)
    :param r:  int, the max distance from the user to the point of interest in km
    :param tags: list[string], the list of tags the user wants the activities to belong to
    :param hist: list of dict, the history of previously selected elements
    :return: list of dict, list of elements consisting of activities and restaurants, ordered by
    appearance in the day.
    
    """

    assert type(day) is int, "Received wrong type"

    day_agenda = []

    fst_half = 2*day
    scd_half = 2*day+1

    activity1, hist = selection_by_tags_distance(fst_half, pos, r, tags, data_activities, hist)
    day_agenda.append(activity1)

    restaurant1, hist = selection_by_tags_distance(fst_half, pos, r, tags, data_restaurants, hist)
    day_agenda.append(restaurant1)

    activity2, hist = selection_by_tags_distance(scd_half, pos, r, tags, data_activities, hist)
    day_agenda.append(activity2)

    restaurant2, hist = selection_by_tags_distance(scd_half, pos, r, tags, data_restaurants, hist)
    day_agenda.append(restaurant2)

    return day_agenda, hist 


def get_distance(lat_x, long_x, lat_y, long_y):
    """
    Get the geo distance between two points on earth

    :param lat_x: float, the latitude of the first point
    :param long_x: float, the longitude of the first point
    :param lat_y: float, the latitude of the second point
    :param long_y: float, the latitude of the second point

    :return float
    """
    return 6371*np.arccos((np.sin(np.radians(lat_x))*np.sin(np.radians(lat_y))) + (np.cos(np.radians(lat_x))*np.cos(np.radians(lat_y))*np.cos(np.radians(long_y-long_x))))


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
    hist = request.headers.get('hist')
    hist = decode(hist)['history'] if (hist != "") else []

    activity, hist = random_selection(time, data_activities, hist)
    if activity == "bof":
        result = {"hist": encode("hist", hist), "activity": {"error": "no more activity not already seen"}}
        return make_response(result,400)
    else:
        result = {"hist": encode("hist", hist), "activity": activity}
        return make_response(result,200)


@swag_from("./docs/swagger_activity_distance.yml")
@app.route("/activity_distance", methods=['GET'])
def get_activity_by_distance():
    time = int(request.args.get('time'))
    lat = float(request.args.get('lat'))
    long = float(request.args.get('long'))
    r = int(request.args.get('r'))
    hist = request.headers.get('hist')
    hist = decode(hist)['history'] if (hist != "") else []

    activity, hist = selection_by_distance(time, (lat,long), r, data_activities, hist)
    if activity == "bof":
        result = {"hist": encode("hist", hist), "activity": {"error": "no more activity not already seen"}}
        return make_response(result,400)
    else:
        result = {"hist": encode("hist", hist), "activity": activity}
        return make_response(result,200)


@swag_from("./docs/swagger_activity_tags_distance.yml")
@app.route("/activity_tags_distance", methods=['GET'])
def get_activity_by_tags_distance():
    time = int(request.args.get('time'))
    lat = float(request.args.get('lat'))
    long = float(request.args.get('long'))
    r = int(request.args.get('r'))
    tags = request.args.get('tags')
    tags = tags.split(",")
    hist = request.headers.get('hist')
    hist = decode(hist)['history'] if (hist != "") else []

    activity, hist = selection_by_tags_distance(time, (lat,long), r, tags, data_activities, hist)
    if activity == "bof":
        result = {"hist": encode("hist", hist), "activity": {"error": "no more activity not already seen"}}
        return make_response(result,400)
    else:
        result = {"hist": encode("hist", hist), "activity": activity}
        return make_response(result,200)


@swag_from("./docs/swagger_restaurant.yml")
@app.route("/restaurant", methods=['GET'])
def get_restaurant():
    time = int(request.args.get('time'))
    hist = request.headers.get('hist')
    hist = decode(hist)['history'] if (hist != "") else []

    restaurant, hist = random_selection(time, data_restaurants, hist)
    if restaurant == "bof":
        result = {"hist": encode("hist", hist), "restaurant":{"error":"no more restaurant not already seen"}}
        return make_response(result, 400)
    else:
        result = {"hist": encode("hist", hist), "restaurant":restaurant}
        return make_response(result, 200)


@swag_from("./docs/swagger_restaurant_distance.yml")
@app.route("/restaurant_distance", methods=['GET'])
def get_restaurant_by_distance():
    time = int(request.args.get('time'))
    lat = float(request.args.get('lat'))
    long = float(request.args.get('long'))
    r = int(request.args.get('r'))
    hist = request.headers.get('hist')
    hist = decode(hist)['history'] if (hist != "") else []

    restaurant, hist = selection_by_distance(time, (lat,long), r, data_restaurants, hist)
    if restaurant == "bof":
        result = {"hist": encode("hist", hist), "restaurant":{"error":"no more restaurant not already seen"}}
        return make_response(result, 400)
    else:
        result = {"hist": encode("hist", hist), "restaurant":restaurant}
        return make_response(result, 200)


@swag_from("./docs/swagger_restaurant_tags_distance.yml")
@app.route("/restaurant_tags_distance", methods=['GET'])
def get_restaurant_by_tags_distance():
    time = int(request.args.get('time'))
    lat = float(request.args.get('lat'))
    long = float(request.args.get('long'))
    r = int(request.args.get('r'))
    tags = request.args.get('tags')
    tags = tags.split(",")
    hist = request.headers.get('hist')
    hist = decode(hist)['history'] if (hist != "") else []

    restaurant, hist = selection_by_tags_distance(time, (lat,long), r, tags, data_restaurants, hist)
    if restaurant == "bof":
        result = {"hist": encode("hist", hist), "restaurant":{"error":"no more restaurant not already seen"}}
        return make_response(result, 400)
    else:
        result = {"hist": encode("hist", hist), "restaurant":restaurant}
        return make_response(result, 200)


@swag_from("./docs/swagger_agenda.yml")
@app.route("/agenda", methods=['GET'])
def get_agenda():
    time = int(request.args.get('time'))
    hist = request.headers.get('hist')
    hist = decode(hist)['history'] if (hist != "") else []

    agenda, hist = basic_agenda(time, hist)
    result = {"hist": encode("hist", hist), "agenda": agenda}
    if "bof" in agenda:
        return make_response(result, 300)
    else:
        return make_response(result,200)


@swag_from("./docs/swagger_agenda_distance.yml")
@app.route("/agenda_distance", methods=['GET'])
def get_agenda_by_distance():
    time = int(request.args.get('time'))
    lat = float(request.args.get('lat'))
    long = float(request.args.get('long'))
    r = int(request.args.get('r'))
    hist = request.headers.get('hist')
    hist = decode(hist)['history'] if (hist != "") else []

    agenda, hist = by_distance_agenda(time, (lat,long), r, hist)
    result = {"hist": encode("hist", hist), "agenda": agenda}
    if "bof" in agenda:
        return make_response(result, 300)
    else:
        return make_response(result,200)

@swag_from("./docs/swagger_agenda_tags_distance.yml")
@app.route("/agenda_tags_distance", methods=['GET'])
def get_agenda_by_tags_distance():
    time = int(request.args.get('time'))
    lat = float(request.args.get('lat'))
    long = float(request.args.get('long'))
    r = int(request.args.get('r'))
    tags = request.args.get('tags')
    tags = tags.split(",")
    hist = request.headers.get('hist')
    hist = decode(hist)['history'] if (hist != "") else []

    agenda, hist = by_tags_distance_agenda(time, (lat,long), r, tags, hist)
    result = {"hist": encode("hist", hist), "agenda": agenda}
    if "bof" in agenda:
        return make_response(result, 300)
    else:
        return make_response(result,200)


@swag_from("./docs/swagger_tags.yml")
@app.route("/tags", methods=['GET'])
def get_tags():
    return make_response({"tags": tag_list}, 200)


if __name__ == "__main__":
    load_data_from_db()
    print(data_restaurants[0])
    preprocessing(data_activities)
    preprocessing(data_restaurants)
    tag_list = get_tag_list()

    app.run(host=HOST, port=PORT)
