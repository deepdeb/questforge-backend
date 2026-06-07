# app/models/quest.py
from sqlalchemy import Column, Integer, String, Boolean, JSON
from app.core.database import Base

class Quest(Base):
    __tablename__ = "quests"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(200))
    xp_reward = Column(Integer, default=25)
    required_level = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    
    # New fields for choice-based quests
    quest_type = Column(String(20), default="simple")  # simple, choice, multi_step
    choices = Column(JSON, nullable=True)  # List of possible choices and outcomes
    story_context = Column(String(300), nullable=True)