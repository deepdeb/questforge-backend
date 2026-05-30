from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AchievementBase(BaseModel):
    name: str
    description: str
    icon: str
    xp_reward: int
    required_level: int

class AchievementResponse(AchievementBase):
    id: int
    unlocked: bool
    unlocked_at: Optional[datetime]

    class Config:
        from_attributes = True