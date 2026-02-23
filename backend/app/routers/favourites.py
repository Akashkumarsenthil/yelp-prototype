from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.favourite import Favourite
from app.models.restaurant import Restaurant
from app.schemas.restaurant import RestaurantOut
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/favourites", tags=["Favourites"])


@router.post("/{restaurant_id}")
def add_favourite(restaurant_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    existing = db.query(Favourite).filter(Favourite.user_id == current_user.id, Favourite.restaurant_id == restaurant_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already in favourites")
    fav = Favourite(user_id=current_user.id, restaurant_id=restaurant_id)
    db.add(fav)
    db.commit()
    return {"message": "Added to favourites"}


@router.delete("/{restaurant_id}")
def remove_favourite(restaurant_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    fav = db.query(Favourite).filter(Favourite.user_id == current_user.id, Favourite.restaurant_id == restaurant_id).first()
    if not fav:
        raise HTTPException(status_code=404, detail="Not in favourites")
    db.delete(fav)
    db.commit()
    return {"message": "Removed from favourites"}


@router.get("/", response_model=List[RestaurantOut])
def get_favourites(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    favs = db.query(Favourite).filter(Favourite.user_id == current_user.id).all()
    restaurant_ids = [f.restaurant_id for f in favs]
    if not restaurant_ids:
        return []
    return db.query(Restaurant).filter(Restaurant.id.in_(restaurant_ids)).all()


@router.get("/check/{restaurant_id}")
def check_favourite(restaurant_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    fav = db.query(Favourite).filter(Favourite.user_id == current_user.id, Favourite.restaurant_id == restaurant_id).first()
    return {"is_favourite": fav is not None}
