from pydantic import BaseModel
from datetime import datetime

class QuestHistoryResponse(BaseModel):
    id: int
    quest_title: str
    xp_rewarded: int
    completed_at: datetime

    class Config:
        from_attributes = True