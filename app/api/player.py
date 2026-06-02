from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.player import PlayerProgress
from app.schemas.player import PlayerProgressResponse

router = APIRouter(prefix="/api/player", tags=["player"])

def calculate_xp_to_next(level: int) -> int:
    return int(100 * (1.5 ** (level - 1)))

@router.get("/", response_model=PlayerProgressResponse)
def get_progress(db: Session = Depends(get_db)):
    try:
        progress = db.query(PlayerProgress).first()
        if not progress:
            progress = PlayerProgress(username="Adventurer")
            db.add(progress)
            db.commit()
            db.refresh(progress)
        # Add computed field
        progress_dict = {
            "username": progress.username,
            "level": progress.level,
            "xp": progress.xp,
            "quests_completed": progress.quests_completed,
            "total_xp_earned": progress.total_xp_earned,
            "xp_to_next": calculate_xp_to_next(progress.level),
            "gold": progress.gold,
            "inventory": progress.inventory
        }
        return progress_dict
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to get player progress: {str(e)}")

@router.post("/gain-xp")
def gain_xp(amount: int, db: Session = Depends(get_db)):
    try:
        progress = db.query(PlayerProgress).first()
        if not progress:
            progress = PlayerProgress(username="Adventurer")
            db.add(progress)
        
        progress.xp += amount
        progress.total_xp_earned += amount
        progress.quests_completed += 1

        xp_to_next = calculate_xp_to_next(progress.level)
        
        if progress.xp >= xp_to_next:
            progress.level += 1
            progress.xp -= xp_to_next

        db.commit()
        db.refresh(progress)
        
        # Return consistent format
        return {
            "message": "Progress updated",
            "progress": {
                "username": progress.username,
                "level": progress.level,
                "xp": progress.xp,
                "quests_completed": progress.quests_completed,
                "total_xp_earned": progress.total_xp_earned,
                "xp_to_next": calculate_xp_to_next(progress.level)
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to gain XP: {str(e)}")
