# Server imports
import json
import time
import requests
from uuid import uuid4
from flask import Flask, jsonify, make_response, request
#Flask app
app = Flask(__name__)

# ------------------------------ ENV variables ------------------------------

#.env imports
from dotenv import load_dotenv
from pathlib import Path
import os

#Getting env variables
dotenv_path = Path('../../.env')
load_dotenv(dotenv_path=dotenv_path)

#Assign env variables

PORT_shop = os.getenv('PORT_SHOP')
HOST = os.getenv('HOST')

# ------------------------------ MODELS ------------------------------

from models import GameStore,Price

# ------------------------------ VARIABLES ------------------------------

PORT = PORT_shop

with open('{}/db/shop.json'.format("."), "r") as jsf:
   shop_dict = json.load(jsf)["gamestores"]
   shop:list[GameStore] = GameStore.schema().load(shop_dict, many=True) 


def generateId():
   return str(uuid4().int)

# ------------------------------ GET & SET FUNCTIONS ------------------------------

def getGameStoreById(shopid):
   for gamestore in shop :
      if gamestore.game_id == shopid :
         return gamestore
   return None

# ------------------------------ ERRORS FUNCTIONS ------------------------------
def notFound(name):
   return make_response(jsonify({'error': f'{name} not found'}),400)


# ------------------------------ ENDPOINTS ------------------------------
@app.route("/", methods=['GET'])
def home():
   return make_response(jsonify({'message':'shop service api root'}))

@app.route("/gamestores", methods=['GET'])
def get_shop():
   return make_response(GameStore.schema().dumps(shop, many=True),200)

@app.route("/gamestores/<gamestore_id>",methods=['GET'])
def get_gamestore_by_id(gamestore_id):
   game_store = getGameStoreById(gamestore_id)
   if game_store : return make_response(game_store.to_json(),200)
   return notFound("game store")

@app.route("/gamestores/<gamestore_id>/prices",methods=['POST'])
def set_price(gamestore_id):
   body = request.json
   try :
      new_price = Price.from_dict(body)
   except :
      sample_request = Price("pokeball",300).to_dict()
      return make_response(jsonify({
         'error': "incorrect request",
         "sample-request-body":sample_request,
         "your-request-body": body
         }),400)

   game_store = getGameStoreById(gamestore_id)
   if not(game_store) : return notFound("shop")
   if new_price in game_store.prices : game_store.prices.remove(new_price)
   game_store.prices.append(new_price)
      
   return make_response(jsonify({'success': 'price updated',"price":new_price.to_dict()}),200)

@app.route("/gamestores/<gamestore_id>/prices/<item_id>",methods=['GET'])
def get_price(gamestore_id,item_id):
   game_store = getGameStoreById(gamestore_id)
   if not(game_store) : return notFound("shop")

   for price in game_store.prices :
      if price.item_id == item_id :
         return make_response(jsonify(price.to_dict()),200)
   return notFound("priceid")
   


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
