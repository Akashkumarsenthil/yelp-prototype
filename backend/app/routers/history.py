from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.review import Review
from app.models.restaurant import Restaurant
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/history", tags=["User History"])


@router.get("/")
def get_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    reviews = db.query(Review).filter(Review.user_id == current_user.id).order_by(Review.created_at.desc()).all()
    review_history = []
    for r in reviews:
        restaurant = db.query(Restaurant).filter(Restaurant.id == r.restaurant_id).first()
        review_history.append({
            "type": "review",
            "review_id": r.id,
            "restaurant_id": r.restaurant_id,
            "restaurant_name": restaurant.name if restaurant else "Unknown",
            "rating": r.rating,
            "comment": r.comment,
            "date": str(r.created_at) if r.created_at else None,
        })

    created_restaurants = db.query(Restaurant).filter(Restaurant.created_by == current_user.id).order_by(Restaurant.created_at.desc()).all()
    restaurant_history = []
    for r in created_restaurants:
        restaurant_history.append({
            "type": "restaurant_added",
            "restaurant_id": r.id,
            "restaurant_name": r.name,
            "date": str(r.created_at) if r.created_at else None,
        })

    combined = review_history + restaurant_history
    combined.sort(key=lambda x: x.get("date") or "", reverse=True)
    return combined
