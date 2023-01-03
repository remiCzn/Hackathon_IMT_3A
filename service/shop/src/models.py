from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Price:
    item_id: str
    item_price: int
    def __hash__(self) -> int:
        return self.item_id
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Price):
            return self.item_id == __o.item_id
        return False

@dataclass_json
@dataclass
class GameStore:
    game_id: str
    prices: list[Price]