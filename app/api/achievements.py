# app/api/achievements.py
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
            db.refresh(player)

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
                player.gold = (player.gold or 50) + ach.xp_reward // 2

        db.commit()
        return achievements
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to load achievements")