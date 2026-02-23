from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.user import User
from app.models.restaurant import Restaurant
from app.models.review import Review
from app.schemas.restaurant import RestaurantOut
from app.schemas.review import ReviewOut
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/owner", tags=["Owner"])


def _require_owner(user: User):
    if user.role != "owner":
        raise HTTPException(status_code=403, detail="Owner access required")


@router.get("/restaurants", response_model=List[RestaurantOut])
def get_owner_restaurants(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _require_owner(current_user)
    return db.query(Restaurant).filter(Restaurant.owner_id == current_user.id).all()


@router.get("/restaurants/{restaurant_id}/reviews", response_model=List[ReviewOut])
def get_restaurant_reviews_owner(restaurant_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _require_owner(current_user)
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id, Restaurant.owner_id == current_user.id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found or not owned by you")
    reviews = db.query(Review).filter(Review.restaurant_id == restaurant_id).order_by(Review.created_at.desc()).all()
    result = []
    for r in reviews:
        user = db.query(User).filter(User.id == r.user_id).first()
        result.append(ReviewOut(
            id=r.id, user_id=r.user_id, restaurant_id=r.restaurant_id,
            rating=r.rating, comment=r.comment, photo_url=r.photo_url,
            created_at=r.created_at, updated_at=r.updated_at,
            user_name=user.name if user else None,
        ))
    return result


@router.get("/dashboard")
def owner_dashboard(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _require_owner(current_user)
    restaurants = db.query(Restaurant).filter(Restaurant.owner_id == current_user.id).all()
    total_reviews = 0
    total_rating_sum = 0.0
    restaurant_stats = []
    for r in restaurants:
        reviews = db.query(Review).filter(Review.restaurant_id == r.id).all()
        count = len(reviews)
        avg = sum(rev.rating for rev in reviews) / count if count > 0 else 0
        total_reviews += count
        total_rating_sum += sum(rev.rating for rev in reviews)

        rating_dist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for rev in reviews:
            rating_dist[rev.rating] = rating_dist.get(rev.rating, 0) + 1

        recent = sorted(reviews, key=lambda x: x.created_at or "", reverse=True)[:5]
        recent_reviews = []
        for rev in recent:
            user = db.query(User).filter(User.id == rev.user_id).first()
            recent_reviews.append({
                "id": rev.id, "rating": rev.rating, "comment": rev.comment,
                "user_name": user.name if user else "Unknown",
                "created_at": str(rev.created_at) if rev.created_at else None,
            })

        restaurant_stats.append({
            "id": r.id, "name": r.name, "average_rating": round(avg, 2),
            "review_count": count, "rating_distribution": rating_dist,
            "recent_reviews": recent_reviews,
        })

    overall_avg = round(total_rating_sum / total_reviews, 2) if total_reviews > 0 else 0
    return {
        "total_restaurants": len(restaurants),
        "total_reviews": total_reviews,
        "overall_average_rating": overall_avg,
        "restaurants": restaurant_stats,
    }
