from flask import Flask, make_response
#from flask_cors import CORS
import random
import json

from dataclasses import dataclass
from typing import NamedTuple

@dataclass
class Item(NamedTuple):
    name: str
    latitude: float
    longitude: float
    tags: list

app = Flask(__name__)
#CORS(app)

PORT = 3001
HOST = '0.0.0.0'

data_activities = []
data_restaurant = []

hist_activities = []
hist_restaurants = []

def load_data():
    global data_activities
    global data_restaurant
    with open('dummy.json', 'r') as activity_file:
        data_activities = json.load(activity_file)
    with open('dummy_restaurant.json', 'r') as restaurant_file:
        data_restaurant = json.load(restaurant_file)


def random_selection(mid_day, data, hist):
    """
    Perform random selection of activity available at that time.

    :param mid_day: integer, an integer representing a half of a day, ranging from 0 to 13
    :return: a dict corresponding to the activity chosen
    """
    assert type(mid_day) is int, "Received wrong type"
    choices = []
    for element in data:
        if element["opened"][mid_day]:
            choices.append(element)

    while len(choices) > 0:
        result = random.choice(choices)
        if result["recordid"] not in hist:
            hist.append(result["recordid"])
            return result

    return "bof"

def basic_agenda(day):

    assert type(day) is int, "Received wrong type"

    day_agenda = []

    fst_half = 2*day
    scd_half = 2*day+1
    day_agenda.append(random_selection(fst_half, data_activities, hist_activities))
    day_agenda.append(random_selection(fst_half, data_restaurant, hist_restaurants))
    day_agenda.append(random_selection(scd_half, data_activities, hist_activities))
    day_agenda.append(random_selection(scd_half, data_restaurant, hist_restaurants))

    return day_agenda



@app.route("/", methods=['GET'])
def home():
    res = {
        "bonjour": "bonjour"
    }
    return make_response(res, 200)

@app.route("/activity", methods=['POST'])
def get_activity(time, position, tags):


    random_selection(time)
    activity = Item()
    return

if __name__ == "__main__":
    load_data()
    print(basic_agenda(0))
    app.run(host=HOST, port=PORT)
