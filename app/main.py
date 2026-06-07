# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base, reset_database
from app.api.player import router as player_router
from app.api.achievements import router as achievements_router
from app.api.quests import router as quests_router
from app.api.shop import router as shop_router
from app.api.history import router as history_router
from app.core.seed import seed_all_data
from app.core.database import get_db

app = FastAPI(title="QuestForge API", version="0.2.0")

# Improved CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5173/",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routers
app.include_router(player_router)
app.include_router(achievements_router)
app.include_router(quests_router)
app.include_router(shop_router)
app.include_router(history_router)

@app.get("/")
async def root():
    return {"message": "QuestForge Backend v0.2 ⚔️"}

# ====================== DEVELOPMENT ONLY ======================
@app.post("/dev/reset")
async def dev_reset_db():
    """Reset database and reseed all data"""
    success = reset_database()
    if success:
        try:
            db = next(get_db())   # Get a database session
            seed_all_data(db)
            return {"status": "success", "message": "Database fully reset and seeded!"}
        except Exception as e:
            return {"status": "warning", "message": f"Reset done, but seeding failed: {str(e)}"}
    return {"status": "error", "message": "Database reset failed."}
# ==============================================================