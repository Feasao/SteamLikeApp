from dataclasses import dataclass
from typing import List

@dataclass
class Game:
    appid: int
    name: str
    genres: List[str]
    img_icon_url: str
    similarity_score: float

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            appid=data["appid"],
            name=data["name"],
            genres=data["genres"],
            img_icon_url=data["img_icon_url"],
            similarity_score=data["similarity_score"]
        )