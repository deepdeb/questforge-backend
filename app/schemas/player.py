from pydantic import BaseModel

class PlayerProgressBase(BaseModel):
    username: str
    level: int
    xp: int
    quests_completed: int
    total_xp_earned: int

class PlayerProgressResponse(PlayerProgressBase):
    xp_to_next: int

    class Config:
        from_attributes = True