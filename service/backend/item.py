from dataclasses import dataclass
from typing import NamedTuple

@dataclass
class Item(NamedTuples):
    name: str
    latitude: float
    longitude: float
    tags: list
