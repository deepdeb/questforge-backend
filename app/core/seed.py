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
            {
                "title": "Daily Login", 
                "description": "Sign in today", 
                "xp_reward": 25, 
                "required_level": 1,
                "quest_type": "simple"
            },
            {
                "title": "Deep Work Session",
                "description": "Focus intensely for 45+ minutes",
                "xp_reward": 45,
                "required_level": 2,
                "quest_type": "choice",
                "choices": [
                    {"id": "focused", "text": "Pure focused work", "xp_reward": 55, "gold_reward": 15, "description": "Maximum productivity"},
                    {"id": "balanced", "text": "Work with short breaks", "xp_reward": 40, "gold_reward": 25, "description": "Sustainable approach"}
                ],
                "story_context": "You sit down to do important work..."
            },
            {
                "title": "Learn Something New",
                "description": "Study a new concept or technology",
                "xp_reward": 50,
                "required_level": 3,
                "quest_type": "choice",
                "choices": [
                    {"id": "deep_dive", "text": "Deep dive into documentation", "xp_reward": 65, "gold_reward": 10},
                    {"id": "hands_on", "text": "Build a small example project", "xp_reward": 55, "gold_reward": 20},
                    {"id": "teach", "text": "Explain it to someone else", "xp_reward": 60, "gold_reward": 15}
                ]
            },
            {
                "title": "Exercise",
                "description": "Move your body",
                "xp_reward": 45,
                "required_level": 4,
                "quest_type": "simple"
            },
        ]
        for q in quests:
            db.add(Quest(**q))
        db.commit()
        print("✅ Quests seeded with choice-based content")

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