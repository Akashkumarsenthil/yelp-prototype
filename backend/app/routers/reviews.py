from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.user import User
from app.models.review import Review
from app.models.restaurant import Restaurant
from app.schemas.review import ReviewCreate, ReviewUpdate, ReviewOut
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/reviews", tags=["Reviews"])


def _recalc_rating(db: Session, restaurant_id: int):
    result = db.query(func.avg(Review.rating), func.count(Review.id)).filter(Review.restaurant_id == restaurant_id).first()
    avg_rating, count = result
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if restaurant:
        restaurant.average_rating = round(float(avg_rating or 0), 2)
        restaurant.review_count = count or 0
        db.commit()


@router.post("/", response_model=ReviewOut, status_code=201)
def create_review(data: ReviewCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    restaurant = db.query(Restaurant).filter(Restaurant.id == data.restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    existing = db.query(Review).filter(Review.user_id == current_user.id, Review.restaurant_id == data.restaurant_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="You have already reviewed this restaurant")
    review = Review(user_id=current_user.id, **data.model_dump())
    db.add(review)
    db.commit()
    db.refresh(review)
    _recalc_rating(db, data.restaurant_id)
    return ReviewOut(
        id=review.id, user_id=review.user_id, restaurant_id=review.restaurant_id,
        rating=review.rating, comment=review.comment, photo_url=review.photo_url,
        created_at=review.created_at, updated_at=review.updated_at, user_name=current_user.name,
    )


@router.get("/restaurant/{restaurant_id}", response_model=List[ReviewOut])
def get_restaurant_reviews(restaurant_id: int, db: Session = Depends(get_db)):
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


@router.put("/{review_id}", response_model=ReviewOut)
def update_review(review_id: int, data: ReviewUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if review.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only edit your own reviews")
    if data.rating is not None:
        review.rating = data.rating
    if data.comment is not None:
        review.comment = data.comment
    db.commit()
    db.refresh(review)
    _recalc_rating(db, review.restaurant_id)
    return ReviewOut(
        id=review.id, user_id=review.user_id, restaurant_id=review.restaurant_id,
        rating=review.rating, comment=review.comment, photo_url=review.photo_url,
        created_at=review.created_at, updated_at=review.updated_at, user_name=current_user.name,
    )


@router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if review.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own reviews")
    restaurant_id = review.restaurant_id
    db.delete(review)
    db.commit()
    _recalc_rating(db, restaurant_id)
    return {"message": "Review deleted"}


@router.get("/user/me", response_model=List[ReviewOut])
def get_my_reviews(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    reviews = db.query(Review).filter(Review.user_id == current_user.id).order_by(Review.created_at.desc()).all()
    return [
        ReviewOut(
            id=r.id, user_id=r.user_id, restaurant_id=r.restaurant_id,
            rating=r.rating, comment=r.comment, photo_url=r.photo_url,
            created_at=r.created_at, updated_at=r.updated_at, user_name=current_user.name,
        ) for r in reviews
    ]
