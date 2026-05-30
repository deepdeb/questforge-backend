from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base

class PlayerProgress(Base):
    __tablename__ = "player_progress"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, default="Adventurer")
    level = Column(Integer, default=1)
    xp = Column(Integer, default=0)
    quests_completed = Column(Integer, default=0)
    total_xp_earned = Column(Integer, default=0)
    achievements_unlocked = Column(Integer, default=0)