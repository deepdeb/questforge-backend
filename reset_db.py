#!/usr/bin/env python3
"""
QuestForge Database Reset Script
Run this to completely reset the database and start fresh.
"""

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def reset_database():
    print("🔄 Starting QuestForge Database Reset...\n")
    
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL not found in .env")
        return

    # Extract database name
    db_name = database_url.split("/")[-1].split("?")[0]
    
    print(f"📊 Target Database: {db_name}")

    try:
        # Connect to MySQL (without specific database)
        base_url = "/".join(database_url.split("/")[:-1])
        engine = create_engine(base_url, pool_pre_ping=True)
        
        with engine.connect() as conn:
            # Drop and recreate database
            conn.execute(text("DROP DATABASE IF EXISTS questforge;"))
            conn.execute(text("CREATE DATABASE questforge CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"))
            print("✅ Database dropped and recreated successfully.")

        # Now connect to the new database
        new_engine = create_engine(database_url, pool_pre_ping=True)
        
        print("🚀 Running Alembic migrations...")
        os.system("alembic upgrade head")
        
        print("\n🎉 Database has been successfully reset!")
        print("You can now start fresh testing.")
        
    except Exception as e:
        print(f"❌ Error during reset: {e}")
        print("\nMake sure:")
        print("   1. MySQL server is running")
        print("   2. Your .env DATABASE_URL is correct")
        print("   3. You have proper MySQL privileges")

if __name__ == "__main__":
    reset_database()