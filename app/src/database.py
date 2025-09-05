import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError
import os

# Pull DATABASE_URL from environment (set in docker-compose.yml)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://banking_user:banking_pass@db:5432/banking_demo")

# Retry until DB is ready
for i in range(5):
    try:
        engine = create_engine(DATABASE_URL)
        break
    except OperationalError:
        print("⏳ Database not ready, retrying in 5s...")
        time.sleep(5)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
