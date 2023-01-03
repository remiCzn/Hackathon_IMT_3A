from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Message:
    username: str
    text: str

@dataclass_json
@dataclass
class Chat:
    uuid:str
    users:list[str]
    messages:list[Message]
