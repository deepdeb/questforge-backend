from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.achievement import Achievement
from app.models.player import PlayerProgress
from app.schemas.achievement import AchievementResponse

router = APIRouter(prefix="/api/achievements", tags=["achievements"])

@router.get("/", response_model=list[AchievementResponse])
def get_achievements(db: Session = Depends(get_db)):
    try:
        achievements = db.query(Achievement).all()
        if not achievements:
            # Seed initial achievements
            seed_achievements(db)
            achievements = db.query(Achievement).all()
        return achievements
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to get achievements: {str(e)}")

def seed_achievements(db: Session):
    initial = [
        {"name": "First Steps", "description": "Complete your first quest", "icon": "🌱", "xp_reward": 50, "required_level": 1},
        {"name": "Rising Star", "description": "Reach Level 3", "icon": "⭐", "xp_reward": 100, "required_level": 3},
        {"name": "Dedicated", "description": "Complete 10 quests", "icon": "🔥", "xp_reward": 150, "required_level": 2},
        {"name": "Legend", "description": "Reach Level 5", "icon": "👑", "xp_reward": 300, "required_level": 5},
    ]
    for ach in initial:
        if not db.query(Achievement).filter_by(name=ach["name"]).first():
            db.add(Achievement(**ach))
    db.commit()