from pydantic import BaseModel

class QuestResponse(BaseModel):
    id: int
    title: str
    description: str
    xp_reward: int
    required_level: int
    is_active: bool

    class Config:
        from_attributes = True