from dataclasses import dataclass
from dataclasses_json import dataclass_json
from enum import Enum

# ------------------------------ POKEMON --------------------------------

@dataclass_json
@dataclass
class PokemonStats :
    pv : int
    power : int
    f_type : str | None
    s_type : str | None
    
@dataclass_json
@dataclass
class Pokemon :
    item_id : str
    name : str
    stats : PokemonStats
