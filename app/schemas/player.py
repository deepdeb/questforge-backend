from pydantic import BaseModel
from typing import Optional

class PlayerProgressBase(BaseModel):
    username: str
    level: int
    xp: int
    quests_completed: int
    total_xp_earned: int

class PlayerProgressResponse(PlayerProgressBase):
    xp_to_next: int
    gold: Optional[int] = 50
    inventory: Optional[str] = "[]" 

    class Config:
        from_attributes = True