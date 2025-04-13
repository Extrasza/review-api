from pydantic import BaseModel

class ReviewInput(BaseModel):
    username: str
    game_name: str
    rating: int
    review: str

class GameNameQuery(BaseModel):
    game_name: str

class ReviewLikeRequest(BaseModel):
    username: str
    game_name: str
