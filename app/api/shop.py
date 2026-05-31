from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.shop import ShopItem
from app.models.player import PlayerProgress
from app.schemas.shop import ShopItemResponse

router = APIRouter(prefix="/api/shop", tags=["shop"])

@router.get("/", response_model=list[ShopItemResponse])
def get_shop_items(db: Session = Depends(get_db)):
    try:
        items = db.query(ShopItem).filter(ShopItem.is_available == True).all()
        if not items:
            seed_shop_items(db)
            items = db.query(ShopItem).filter(ShopItem.is_available == True).all()
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch shop items")

def seed_shop_items(db: Session):
    items = [
        {"name": "XP Potion", "description": "Gain 100 bonus XP", "price": 60, "icon": "🧪", "effect": "xp_boost"},
        {"name": "Legendary Sword", "description": "Cosmetic title upgrade", "price": 150, "icon": "⚔️", "effect": "cosmetic"},
        {"name": "Lucky Charm", "description": "Next 3 quests give +20% XP", "price": 90, "icon": "🍀", "effect": "boost"},
        {"name": "Mystic Robe", "description": "Premium avatar frame", "price": 120, "icon": "🧥", "effect": "cosmetic"},
    ]
    for item in items:
        if not db.query(ShopItem).filter_by(name=item["name"]).first():
            db.add(ShopItem(**item))
    db.commit()