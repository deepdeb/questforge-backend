# app/api/quests.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.quest import Quest
from app.schemas.quest import QuestResponse

router = APIRouter(prefix="/api/quests", tags=["quests"])

@router.get("/", response_model=list[QuestResponse])
def get_quests(db: Session = Depends(get_db)):
    try:
        quests = db.query(Quest).filter(Quest.is_active == True).all()
        return quests
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while fetching quests."
        )