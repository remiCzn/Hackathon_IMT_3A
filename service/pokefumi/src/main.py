# Server imports
import json
import time
import requests
from uuid import uuid4
import random
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
PORT_pokefumi = os.getenv('PORT_POKEFUMI')
HOST = os.getenv('HOST')

# ------------------------------ MODELS ------------------------------

from models import Round,Match,PokemonStats,Pokemon,DualPlayers,Move

# ------------------------------ VARIABLES ------------------------------

PORT = PORT_pokefumi

with open('{}/db/matches.json'.format("."), "r") as jsf:
   file_json = json.load(jsf)
   matches_dict = file_json["matches"]
   matches:list[Match] = Match.schema().load(matches_dict, many=True) 
   
   past_matches_dict = file_json["past_matches"]
   past_matches:list[Match] = Match.schema().load(past_matches_dict, many=True) 


with open('{}/db/pokemon.json'.format("."), "r") as jsf:
   pokemons_dict = json.load(jsf)
   pokemons:list[Pokemon] = Pokemon.schema().load(pokemons_dict, many=True) 


def generateId():
   return str(uuid4().int)

# ------------------------------ GET & SET FUNCTIONS ------------------------------

def getMatchById(matchid):
   for match in matches :
      if match.match_id == matchid :
         return match
   return None

def getPokemonById(pokemonid):
   for pokemon in pokemons :
      if pokemon.item_id == pokemonid :
         return pokemon
   return None

# ------------------------------ POKEMONS RELATED FUNCS ------------------------------

# create a dict with pokemon weakness relative to the type
pokemon_weakness = {
   "fire" : ["water","ground","rock"],
   "water" : ["grass","electric"],
   "grass" : ["fire","ice","poison","flying","bug"],
   "electric" : ["ground"],
   "ice" : ["fire","fighting","rock","steel"],
   "fighting" : ["flying","psychic","fairy"],
   "poison" : ["ground","psychic"],
   "ground" : ["water","grass","ice"],
   "flying" : ["electric","ice","rock"],
   "psychic" : ["bug","ghost","dark"],
   "bug" : ["fire","flying","rock"],
   "rock" : ["water","grass","fighting","ground","steel"],
   "ghost" : ["ghost","dark"],
   "dragon" : ["ice","dragon","fairy"],
   "dark" : ["fighting","bug","fairy"],
   "steel" : ["fire","fighting","ground"],
   "fairy" : ["poison","steel"]
}

def pokemonStrength(pokemon1,pokemon2):
   """Return a number based on the stats of the first given pokemon on the second, more the number is high, more the first pokemon is strong"""
   pokemon2_weakness = (pokemon_weakness[pokemon2.stats.f_type] if pokemon2.stats.f_type != None else []) + (pokemon_weakness[pokemon2.stats.s_type] if pokemon2.stats.s_type != None else [])
   pokemon_1_effectiveness = sum([1 for _type in [pokemon1.stats.f_type,pokemon1.stats.s_type] if _type in pokemon2_weakness])
   pokemon_1_totalforce = pokemon1.stats.pv + pokemon1.stats.power*(1+pokemon_1_effectiveness/2)
   return pokemon_1_totalforce


def determineBestPokemon(pokemon1,pokemon2):
   """Determine the best pokemon between pokemon1 and pokemon2"""
   pokemon1_score = pokemonStrength(pokemon1,pokemon2)
   pokemon2_score = pokemonStrength(pokemon2,pokemon1)
   if pokemon1_score > pokemon2_score:
      return 1
   elif pokemon1_score < pokemon2_score:
      return 2
   else :
      return random.randint(1,2)
# ------------------------------ ERRORS FUNCTIONS ------------------------------
def notFound(name):
   return make_response(jsonify({'error': f'{name} not found'}),400)

def checkNot3Matches():
   """Check if the player has less than 3 matches"""
   return True

# ------------------------------ ENDPOINTS ------------------------------
@app.route("/", methods=['GET'])
def home():
   return make_response(jsonify({'message':'shop service api root'}))

@app.route("/matches", methods=['GET'])
def get_match():
   return make_response(Match.schema().dumps(matches, many=True),200)

@app.route("/matches/<matchid>",methods=['GET'])
def get_match_by_id(matchid):
   match = getMatchById(matchid)
   if match : return make_response(match.to_json(),200)
   return notFound("match")

@app.route("/matches",methods=['POST'])
def create_match():
   """
   need :
   player1
   player2

   check :
   pour chaque joueurs ceux-ci n'ont pas plus de 3 matchs simultanés
   """
   if not checkNot3Matches() : return make_response(jsonify({'error': 'a player already has 3 matches occuring'}),400)

   body = request.json
   try :
      players = DualPlayers.from_dict(body)
   except :
      sample_request = DualPlayers("player1","player2").to_dict()
      return make_response(jsonify({
         'error': "incorrect request",
         "sample-request-body":sample_request,
         "your-request-body": body
         }),400)

   new_match = Match(
      match_id=str(uuid4().int),
      status="CREATED",
      round_history=[],
      players=players,
      current_round=Round(
         player1_item_used=None,
         player2_item_used=None,
         winner=None
      ),
      winner=None
   )

   matches.append(new_match)

   return make_response(jsonify({'success': 'match created',"match":new_match.to_dict()}),200)

@app.route("/matches/<match_id>/play",methods=['GET'])
def who_need_to_play(match_id):
   match = getMatchById(match_id)
   if not(match) : return notFound("match")

   liste = []
   current_round = match.current_round
   if not(current_round.player1_item_used) : liste.append(match.players.player1)
   if not(current_round.player2_item_used) : liste.append(match.players.player2)

   return make_response(jsonify({'who_need_to_play': liste}),200)

@app.route("/matches/<match_id>/play",methods=['POST'])
def play_pokemon(match_id):
   """
   need :
   item_id
   player_id
   
   check :
   if the match is valid | ok
   if the player is valid | ok
   
   if the player has already played | ok
   if the item is in player's inventory
   """
   #check if the match is valid
   match = getMatchById(match_id)
   if not(match) : return notFound("match")

   #check if the player is valid
   body = request.json
   try :
      player_move:Move = Move.from_dict(body)
   except :
      sample_request = Move("player1","pikachu1234","pikachu").to_dict()
      return make_response(jsonify({
         'error': "incorrect request",
         "sample-request-body":sample_request,
         "your-request-body": body
         }),400)
   players:DualPlayers = match.players
   if not(players.contains(player_move.player_id)) : return notFound("player")
   player_key = players.get_key(player_move.player_id)

   #check if the player has already played
   current_round = match.current_round
   if getattr(current_round,player_key+"_item_used") : return make_response(jsonify({'error': 'the player has already played'}),400)
   else :
      #TODO CHECK IF THE ITEM IS IN PLAYER'S INVENTORY
      #TODO CHECK IF THE ITEM IS A POKEMON

      setattr(current_round,player_key+"_item_used",player_move.in_game_item_id)

      if (current_round.player1_item_used and current_round.player2_item_used) :

         #determine the winner
         pokemon1 = getPokemonById(current_round.player1_item_used)
         pokemon2 = getPokemonById(current_round.player2_item_used)
         winner = determineBestPokemon(pokemon1,pokemon2)
         current_round.winner = winner

         match.round_history.append(current_round)
         match.current_round = Round(
            player1_item_used=None,
            player2_item_used=None,
            winner=None
         )

         # if all the rounds are finished
         if len(match.round_history) == 3 :
            match.status = "FINISHED"
            match.winner = 1 if len([_round for _round in match.round_history if _round.winner == 1]) > 1 else 2
            past_matches.append(match)
            matches.remove(match)

         return make_response(jsonify({'success': 'player played','pokemon_played':player_move.in_game_item_id,'result':current_round.to_dict()}),200)
      
      return make_response(jsonify({'success': 'player played','pokemon_played':player_move.in_game_item_id,'result':'waiting for the opponent to play'}),200)




if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)