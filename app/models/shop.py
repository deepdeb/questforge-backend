from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base

class ShopItem(Base):
    __tablename__ = "shop_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False)
    description = Column(String(200))
    price = Column(Integer, nullable=False)
    icon = Column(String(20))
    effect = Column(String(50), default="cosmetic")  # xp_boost, title, etc.
    is_available = Column(Boolean, default=True)