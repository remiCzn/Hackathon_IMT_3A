from flask import Flask, make_response, request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from
#from flask_cors import CORS
import numpy as np
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
            "categorie" : result["fields"]["categorie"]
        }
            return res

    return "bof"


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
        if element["opened"][mid_day]:
            dist = get_distance(pos[0], pos[1], element["fields"]["localisation"][0], element["fields"]["localisation"][1])
            if dist <= r:
                choices.append(element)
    
    while len(choices) > 0:
        rand_id = random.randint(0, len(choices)-1)
        result = choices.pop(rand_id)
        if result["recordid"] not in hist:
            hist.append(result["recordid"])
            res = {
            "name" : result["fields"]["nom_complet"],
            "adress" : result["fields"]["adresse"],
            "categorie" : result["fields"]["categorie"]
        }
            return res

    return "bof"


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
        if element["opened"][mid_day]:
            dist = get_distance(pos[0], pos[1], element["fields"]["localisation"][0], element["fields"]["localisation"][1])
            if (dist <= r) & (element["fields"]["categorie"] in tags):
                choices.append(element)

    while len(choices) > 0:
        rand_id = random.randint(0, len(choices)-1)
        result = choices.pop(rand_id)
        if result["recordid"] not in hist:
            hist.append(result["recordid"])
            res = {
            "name" : result["fields"]["nom_complet"],
            "adress" : result["fields"]["adresse"],
            "categorie" : result["fields"]["categorie"]
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


def by_distance_agenda(day, pos, r):
    """
    Create an agenda respecting a distance criterion consisting of randomly
    selected activities and restaurant for the first half and second half of the day and 
    for lunch and dinner.
    :param day: int, ranging from 0 to 6, the day for which the function aims at creating an agenda
    :param pos: tuple(float, float), a tuple containing the latitude and the longitude of the user such that pos = (lat, long)
    :param r:  int, the max distance from the user to the point of interest in km
    :return: list of dict, list of elements consisting of activities and restaurants, ordered by
    appearance in the day.
    """

    assert type(day) is int, "Received wrong type"

    day_agenda = []

    fst_half = 2*day
    scd_half = 2*day+1
    day_agenda.append(selection_by_distance(fst_half, pos, r, data_activities, hist_activities))
    day_agenda.append(selection_by_distance(fst_half, pos, r, data_restaurants, hist_restaurants))
    day_agenda.append(selection_by_distance(scd_half, pos, r, data_activities, hist_activities))
    day_agenda.append(selection_by_distance(scd_half, pos, r, data_restaurants, hist_restaurants))

    return day_agenda


def by_tags_distance_agenda(day, pos, r, tags):
    """
    Create an agenda respecting a distance criterion and tags criteria, consisting of randomly
    selected activities and restaurant for the first half and second half of the day and 
    for lunch and dinner.
    :param day: int, ranging from 0 to 6, the day for which the function aims at creating an agenda
    :param pos: tuple(float, float), a tuple containing the latitude and the longitude of the user such that pos = (lat, long)
    :param r:  int, the max distance from the user to the point of interest in km
    :param tags: list[string], the list of tags the user wants the activities to belong to
    :return: list of dict, list of elements consisting of activities and restaurants, ordered by
    appearance in the day.
    
    """

    assert type(day) is int, "Received wrong type"

    day_agenda = []

    fst_half = 2*day
    scd_half = 2*day+1
    day_agenda.append(selection_by_tags_distance(fst_half, pos, r, tags, data_activities, hist_activities))
    day_agenda.append(selection_by_tags_distance(fst_half, pos, r, tags, data_restaurants, hist_restaurants))
    day_agenda.append(selection_by_tags_distance(scd_half, pos, r, tags, data_activities, hist_activities))
    day_agenda.append(selection_by_tags_distance(scd_half, pos, r, tags, data_restaurants, hist_restaurants))

    return day_agenda


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
    activity = random_selection(time, data_activities, hist_activities)
    if activity == "bof":
        result = {"error": "no more activity not already seen"}
        return make_response(result,400)
    else:
        return make_response(activity,200)


@swag_from("./docs/swagger_activity_distance.yml")
@app.route("/activity_distance", methods=['GET'])
def get_activity_by_distance():
    time = int(request.args.get('time'))
    lat = float(request.args.get('lat'))
    long = float(request.args.get('long'))
    r = int(request.args.get('r'))
    activity = selection_by_distance(time, (lat,long), r, data_activities, hist_activities)
    if activity == "bof":
        result = {"error": "no more activity not already seen"}
        return make_response(result,400)
    else:
        return make_response(activity,200)


@swag_from("./docs/swagger_activity_tags_distance.yml")
@app.route("/activity_tags_distance", methods=['GET'])
def get_activity_by_tags_distance():
    time = int(request.args.get('time'))
    lat = float(request.args.get('lat'))
    long = float(request.args.get('long'))
    r = int(request.args.get('r'))
    tags = request.args.get('tags')
    tags = tags.split(",")
    activity = selection_by_tags_distance(time, (lat,long), r, tags, data_activities, hist_activities)
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


@swag_from("./docs/swagger_restaurant_distance.yml")
@app.route("/restaurant_distance", methods=['GET'])
def get_restaurant_by_distance():
    time = int(request.args.get('time'))
    lat = float(request.args.get('lat'))
    long = float(request.args.get('long'))
    r = int(request.args.get('r'))
    activity = selection_by_distance(time, (lat,long), r, data_restaurants, hist_restaurants)
    if activity == "bof":
        result = {"error": "no more activity not already seen"}
        return make_response(result,400)
    else:
        return make_response(activity,200)


@swag_from("./docs/swagger_restaurant_tags_distance.yml")
@app.route("/restaurant_tags_distance", methods=['GET'])
def get_restaurant_by_tags_distance():
    time = int(request.args.get('time'))
    lat = float(request.args.get('lat'))
    long = float(request.args.get('long'))
    r = int(request.args.get('r'))
    tags = request.args.get('tags')
    tags = tags.split(",")
    activity = selection_by_tags_distance(time, (lat,long), r, tags, data_restaurants, hist_restaurants)
    if activity == "bof":
        result = {"error": "no more activity not already seen"}
        return make_response(result,400)
    else:
        return make_response(activity,200)


@swag_from("./docs/swagger_agenda.yml")
@app.route("/agenda", methods=['GET'])
def get_agenda():
    time = int(request.args.get('time'))
    agenda = basic_agenda(time)
    if "bof" in agenda:
        return make_response(agenda, 300)
    else:
        return make_response(agenda,200)


@swag_from("./docs/swagger_agenda_distance.yml")
@app.route("/agenda_distance", methods=['GET'])
def get_agenda_by_distance():
    time = int(request.args.get('time'))
    lat = float(request.args.get('lat'))
    long = float(request.args.get('long'))
    r = int(request.args.get('r'))

    agenda = by_distance_agenda(time, (lat,long), r)
    if "bof" in agenda:
        return make_response(agenda, 300)
    else:
        return make_response(agenda, 200)

@swag_from("./docs/swagger_agenda_tags_distance.yml")
@app.route("/agenda_tags_distance", methods=['GET'])
def get_agenda_by_tags_distance():
    time = int(request.args.get('time'))
    lat = float(request.args.get('lat'))
    long = float(request.args.get('long'))
    r = int(request.args.get('r'))
    tags = request.args.get('tags')
    tags = tags.split(",")

    agenda = by_tags_distance_agenda(time, (lat,long), r, tags)
    if "bof" in agenda:
        return make_response(agenda, 300)
    else:
        return make_response(agenda, 200)


@swag_from("./docs/swagger_tags.yml")
@app.route("/tags", methods=['GET'])
def get_tags():
    return make_response({"tags": tag_list}, 200)




if __name__ == "__main__":
    load_data()
    app.run(host=HOST, port=PORT)
