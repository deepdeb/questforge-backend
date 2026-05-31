from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base

class Quest(Base):
    __tablename__ = "quests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    description = Column(String(200))
    xp_reward = Column(Integer)
    required_level = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)