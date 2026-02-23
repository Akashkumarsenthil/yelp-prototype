import os
import uuid
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database import get_db
from app.models.user import User
from app.models.restaurant import Restaurant
from app.models.restaurant_photo import RestaurantPhoto
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate, RestaurantOut
from app.utils.auth import get_current_user, get_optional_user

router = APIRouter(prefix="/api/restaurants", tags=["Restaurants"])

UPLOAD_DIR = "uploads/restaurants"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/", response_model=RestaurantOut, status_code=201)
def create_restaurant(data: RestaurantCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    restaurant = Restaurant(**data.model_dump(), created_by=current_user.id)
    if current_user.role == "owner":
        restaurant.owner_id = current_user.id
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return restaurant


@router.get("/", response_model=List[RestaurantOut])
def list_restaurants(
    name: Optional[str] = Query(None),
    cuisine_type: Optional[str] = Query(None),
    keywords: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    zip_code: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    query = db.query(Restaurant)
    if name:
        query = query.filter(Restaurant.name.ilike(f"%{name}%"))
    if cuisine_type:
        query = query.filter(Restaurant.cuisine_type.ilike(f"%{cuisine_type}%"))
    if city:
        query = query.filter(Restaurant.city.ilike(f"%{city}%"))
    if zip_code:
        query = query.filter(Restaurant.zip_code == zip_code)
    if keywords:
        kw = f"%{keywords}%"
        query = query.filter(
            or_(
                Restaurant.description.ilike(kw),
                Restaurant.amenities.ilike(kw),
                Restaurant.ambiance.ilike(kw),
                Restaurant.name.ilike(kw),
            )
        )
    return query.offset(skip).limit(limit).all()


@router.get("/{restaurant_id}", response_model=RestaurantOut)
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant


@router.put("/{restaurant_id}", response_model=RestaurantOut)
def update_restaurant(
    restaurant_id: int,
    data: RestaurantUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    if restaurant.owner_id != current_user.id and restaurant.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this restaurant")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(restaurant, key, value)
    db.commit()
    db.refresh(restaurant)
    return restaurant


@router.post("/{restaurant_id}/claim", response_model=RestaurantOut)
def claim_restaurant(restaurant_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "owner":
        raise HTTPException(status_code=403, detail="Only owners can claim restaurants")
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    if restaurant.owner_id:
        raise HTTPException(status_code=400, detail="Restaurant already claimed")
    restaurant.owner_id = current_user.id
    db.commit()
    db.refresh(restaurant)
    return restaurant


@router.post("/{restaurant_id}/photos")
async def upload_restaurant_photo(
    restaurant_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    ext = file.filename.split(".")[-1] if file.filename else "jpg"
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    contents = await file.read()
    with open(filepath, "wb") as f:
        f.write(contents)
    photo = RestaurantPhoto(restaurant_id=restaurant_id, photo_url=f"/uploads/restaurants/{filename}")
    db.add(photo)
    db.commit()
    return {"photo_url": photo.photo_url}
