from fastapi import FastAPI, Depends
from pydantic import BaseModel
from services import get_db, Item
from sqlalchemy.orm import Session
from datetime import datetime

app = FastAPI()

# Pydantic schema for request validation
class ItemCreate(BaseModel):
    title: str
    video_id: str
    description: str
    thumbnail_url: bool


@app.get("/movies")
def get_all_movies(db: Session = Depends(get_db)):
    movies = db.query(Item).all()
    return {"movies": movies}

@app.post("/movie")
def movie(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(
        title=item.title,
        video_id=item.video_id,
        descrption=item.description,
        thumbnail_url=item.thumbnail_url,
        created_at=datetime.now(),  # Manually set timestamps
        updated_at=datetime.now(),
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"message": f"Movie '{db_item.title}' created!", "movie": db_item}


