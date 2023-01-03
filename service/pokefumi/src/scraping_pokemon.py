# Json
import requests
import json

# Types
from models import PokemonStats,Pokemon

# Loading
from time import sleep
from tqdm import tqdm


if __name__ == "__main__":
    ids = range(1,906)

    pokemons = []

    for id in tqdm(ids):
        url = f"https://pokeapi.co/api/v2/pokemon/{id}"
        response = requests.get(url).json()
        pokemon = Pokemon(
            item_id = str(id),
            name=response["name"],
            stats=PokemonStats(
                pv=response["stats"][0]["base_stat"],
                power=response["stats"][1]["base_stat"],
                f_type=response["types"][0]["type"]["name"],
                s_type=response["types"][1]["type"]["name"] if len(response["types"]) > 1 else None
            )
        )
        pokemons.append(pokemon)
        sleep(0.1)

    # Save pokemons in a json file
    with open('{}/db/pokemon.json'.format("."), 'w') as outfile:
        json.dump(Pokemon.schema().dump(pokemons, many=True), outfile)