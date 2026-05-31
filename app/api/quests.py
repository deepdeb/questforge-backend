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

        if not quests:
            seed_quests(db)
            quests = db.query(Quest).filter(Quest.is_active == True).all()

        return quests

    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail="An error occurred while fetching quests."
        )


def seed_quests(db: Session):
    """Separate seeding function with its own error handling"""
    try:
        initial_quests = [
            {"title": "Daily Login", "description": "Sign in today", "xp_reward": 25, "required_level": 1},
            {"title": "Complete a Task", "description": "Finish any productive task", "xp_reward": 35, "required_level": 1},
            {"title": "Write a Journal Entry", "description": "Reflect on your day", "xp_reward": 40, "required_level": 2},
            {"title": "Learn Something New", "description": "Study for 20+ minutes", "xp_reward": 50, "required_level": 3},
            {"title": "Exercise", "description": "Move your body", "xp_reward": 45, "required_level": 4},
        ]

        for q in initial_quests:
            if not db.query(Quest).filter_by(title=q["title"]).first():
                db.add(Quest(**q))

        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Warning: Seeding quests failed: {e}")  # Don't expose to user
        # Optionally raise, but usually we want the endpoint to still work