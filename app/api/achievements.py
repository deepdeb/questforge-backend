from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.achievement import Achievement
from app.models.player import PlayerProgress
from app.schemas.achievement import AchievementResponse
from datetime import datetime

router = APIRouter(prefix="/api/achievements", tags=["achievements"])

@router.get("/", response_model=list[AchievementResponse])
def get_achievements(db: Session = Depends(get_db)):
    try:
        player = db.query(PlayerProgress).first()
        if not player:
            player = PlayerProgress(username="Adventurer")
            db.add(player)
            db.commit()

        achievements = db.query(Achievement).all()
        if not achievements:
            seed_achievements(db)
            achievements = db.query(Achievement).all()

        # Auto-unlock logic
        for ach in achievements:
            if ach.unlocked:
                continue
                
            should_unlock = False
            if ach.name == "First Steps" and player.quests_completed >= 1:
                should_unlock = True
            elif ach.name == "Rising Star" and player.level >= 3:
                should_unlock = True
            elif ach.name == "Dedicated" and player.quests_completed >= 10:
                should_unlock = True
            elif ach.name == "Legend" and player.level >= 5:
                should_unlock = True

            if should_unlock:
                ach.unlocked = True
                ach.unlocked_at = datetime.utcnow()
                player.achievements_unlocked = (player.achievements_unlocked or 0) + 1
                player.gold = (player.gold or 50) + ach.xp_reward // 2   # Bonus gold

        db.commit()
        return achievements
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to load achievements")

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