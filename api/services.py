import os

from sqlalchemy import Column, Integer, String, Float, Boolean, create_engine, Date, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get `api/` directory
DB_PATH = os.path.join(BASE_DIR, "../moviesdb.db")  # Move one level up to `main/`
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Item(Base):
    __tablename__ = "MoviesDatabase"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    video_id = Column(String, index=True)
    created_at = Column(Date, server_default=func.now())
    updated_at = Column(Date, server_default=func.now())
    descrption = Column(String)
    thumbnail_url = Column(String, default=True)

# Create tables in the database
Base.metadata.create_all(bind=engine)