from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.player import PlayerProgress
from app.models.history import QuestHistory
from app.schemas.history import QuestHistoryResponse

router = APIRouter(prefix="/api/history", tags=["history"])

@router.get("/", response_model=list[QuestHistoryResponse])
def get_history(db: Session = Depends(get_db)):
    try:
        player = db.query(PlayerProgress).first()
        if not player:
            return []
        
        history = db.query(QuestHistory).filter(
            QuestHistory.player_id == player.id
        ).order_by(QuestHistory.completed_at.desc()).all()
        
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch history")