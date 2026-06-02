from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class QuestHistory(Base):
    __tablename__ = "quest_history"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("player_progress.id"))
    quest_title = Column(String(100))
    xp_rewarded = Column(Integer)
    completed_at = Column(DateTime, default=datetime.utcnow)

    player = relationship("PlayerProgress", back_populates="history")