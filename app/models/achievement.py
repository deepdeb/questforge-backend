from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.core.database import Base

class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True)
    description = Column(String(200))
    icon = Column(String(50))
    xp_reward = Column(Integer, default=50)
    required_level = Column(Integer, default=1)
    unlocked = Column(Boolean, default=False)
    unlocked_at = Column(DateTime, nullable=True)