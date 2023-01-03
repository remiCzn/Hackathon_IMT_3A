from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class GameStats:
    game_id: str
    win:int
    lose:int

@dataclass_json
@dataclass
class Stats:
    username: str
    gamestats:list[GameStats]

    def getGameStatsById(self, game_id:str):
        for gamestat in self.gamestats:
            if gamestat.game_id == game_id:
                return gamestat
        return None

@dataclass_json
@dataclass
class StatAndUser:
    username: str
    game_id: str