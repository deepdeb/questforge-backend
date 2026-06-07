# app/core/seed.py
from sqlalchemy.orm import Session
from app.models.player import PlayerProgress
from app.models.quest import Quest
from app.models.achievement import Achievement
from app.models.shop import ShopItem

def seed_all_data(db: Session):
    """Centralized seeding function - run after DB reset"""
    print("🌱 Starting database seeding...")

    # Seed Player
    player = db.query(PlayerProgress).first()
    if not player:
        player = PlayerProgress(username="Adventurer")
        db.add(player)
        db.commit()
        db.refresh(player)
        print("✅ Player created")

    # Seed Quests
    if db.query(Quest).count() == 0:
        quests = [
            {"title": "Daily Login", "description": "Sign in today", "xp_reward": 25, "required_level": 1},
            {"title": "Complete a Task", "description": "Finish any productive task", "xp_reward": 35, "required_level": 1},
            {"title": "Write a Journal Entry", "description": "Reflect on your day", "xp_reward": 40, "required_level": 2},
            {"title": "Learn Something New", "description": "Study for 20+ minutes", "xp_reward": 50, "required_level": 3},
            {"title": "Exercise", "description": "Move your body", "xp_reward": 45, "required_level": 4},
        ]
        for q in quests:
            db.add(Quest(**q))
        db.commit()
        print("✅ Quests seeded")

    # Seed Achievements
    if db.query(Achievement).count() == 0:
        achievements = [
            {"name": "First Steps", "description": "Complete your first quest", "icon": "🌱", "xp_reward": 50, "required_level": 1},
            {"name": "Rising Star", "description": "Reach Level 3", "icon": "⭐", "xp_reward": 100, "required_level": 3},
            {"name": "Dedicated", "description": "Complete 10 quests", "icon": "🔥", "xp_reward": 150, "required_level": 2},
            {"name": "Legend", "description": "Reach Level 5", "icon": "👑", "xp_reward": 300, "required_level": 5},
        ]
        for ach in achievements:
            db.add(Achievement(**ach))
        db.commit()
        print("✅ Achievements seeded")

    # Seed Shop Items
    if db.query(ShopItem).count() == 0:
        items = [
            {"name": "XP Potion", "description": "Gain 100 bonus XP", "price": 60, "icon": "🧪", "effect": "xp_boost"},
            {"name": "Legendary Sword", "description": "Cosmetic title upgrade", "price": 150, "icon": "⚔️", "effect": "cosmetic"},
            {"name": "Lucky Charm", "description": "Next 3 quests give +20% XP", "price": 90, "icon": "🍀", "effect": "boost"},
            {"name": "Mystic Robe", "description": "Premium avatar frame", "price": 120, "icon": "🧥", "effect": "cosmetic"},
        ]
        for item in items:
            db.add(ShopItem(**item))
        db.commit()
        print("✅ Shop items seeded")

    print("🎉 All seeding completed!")