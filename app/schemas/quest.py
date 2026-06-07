# app/schemas/quest.py
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class QuestChoice(BaseModel):
    id: str
    text: str
    xp_reward: int
    gold_reward: int = 0
    description: Optional[str] = None

class QuestResponse(BaseModel):
    id: int
    title: str
    description: str
    xp_reward: int
    required_level: int
    is_active: bool
    quest_type: str
    choices: Optional[List[Dict[str, Any]]] = None
    story_context: Optional[str] = None

    class Config:
        from_attributes = True