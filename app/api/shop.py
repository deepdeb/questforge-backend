from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.shop import ShopItem
from app.models.player import PlayerProgress
from app.schemas.shop import ShopItemResponse, PurchaseRequest
from datetime import datetime

router = APIRouter(prefix="/api/shop", tags=["shop"])

@router.get("/", response_model=list[ShopItemResponse])
def get_shop_items(db: Session = Depends(get_db)):
    try:
        items = db.query(ShopItem).filter(ShopItem.is_available == True).all()
        if not items:
            seed_shop_items(db)
            items = db.query(ShopItem).filter(ShopItem.is_available == True).all()
        return items
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch shop items")

@router.post("/purchase")
def purchase_item(request: PurchaseRequest, db: Session = Depends(get_db)):
    try:
        # Get player
        player = db.query(PlayerProgress).first()
        if not player:
            raise HTTPException(status_code=404, detail="Player not found")

        # Get item
        item = db.query(ShopItem).filter(ShopItem.id == request.item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        if player.gold < item.price:
            raise HTTPException(status_code=400, detail="Not enough gold")

        # Process purchase
        player.gold -= item.price
        
        import json
        try:
            current_inventory = json.loads(player.inventory or "[]")
        except:
            current_inventory = []
            
        current_inventory.append({
            "item_id": item.id,
            "name": item.name,
            "icon": item.icon,
            "purchased_at": str(datetime.utcnow())
        })
        
        player.inventory = json.dumps(current_inventory)
        
        db.commit()
        db.refresh(player)

        return {
            "success": True,
            "message": f"Purchased {item.name} successfully!",
            "new_gold": player.gold
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Purchase failed")

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