# Define shop price based on pokemon strength and hp and save them in a json file

# Json
import requests
import json

# Types
from pokemon_models import PokemonStats, Pokemon
import models as shop_models

# Loading
from time import sleep
from tqdm import tqdm


# Return the price of the pokemon based on its stats
def get_pokemon_price(pokemon: Pokemon) -> int:
    return pokemon.stats.pv + pokemon.stats.power if pokemon.stats.power > 20 else 0


if __name__ == "__main__":
    # Get pokemon list
    with  open ( 'pokemon.json' ,  'r' )  as  f:
        pokemons_dict = json.load(f)
        pokemons:list[Pokemon] = Pokemon.schema().load(pokemons_dict, many=True)

    with open('shop.json', 'w') as f:
        pokemons_prices = []
        for pokemon in tqdm(pokemons):
            pokemon_price = get_pokemon_price(pokemon)
            pokemon_price = shop_models.Price(pokemon.item_id, pokemon_price)
            pokemons_prices.append(pokemon_price)

        json.dump({"gamestores":[shop_models.GameStore('pokefumi', pokemons_prices).to_dict()]}, f)
            