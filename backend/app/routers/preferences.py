import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.preference import UserPreference
from app.schemas.preference import PreferenceUpdate, PreferenceOut
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/preferences", tags=["User Preferences"])


@router.get("/", response_model=PreferenceOut)
def get_preferences(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    pref = db.query(UserPreference).filter(UserPreference.user_id == current_user.id).first()
    if not pref:
        pref = UserPreference(user_id=current_user.id)
        db.add(pref)
        db.commit()
        db.refresh(pref)
    return pref


@router.put("/", response_model=PreferenceOut)
def update_preferences(data: PreferenceUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    pref = db.query(UserPreference).filter(UserPreference.user_id == current_user.id).first()
    if not pref:
        pref = UserPreference(user_id=current_user.id)
        db.add(pref)
    if data.cuisine_preferences is not None:
        pref.cuisine_preferences = json.dumps(data.cuisine_preferences)
    if data.price_range is not None:
        pref.price_range = data.price_range
    if data.preferred_locations is not None:
        pref.preferred_locations = json.dumps(data.preferred_locations)
    if data.search_radius is not None:
        pref.search_radius = data.search_radius
    if data.dietary_needs is not None:
        pref.dietary_needs = json.dumps(data.dietary_needs)
    if data.ambiance_preferences is not None:
        pref.ambiance_preferences = json.dumps(data.ambiance_preferences)
    if data.sort_preference is not None:
        pref.sort_preference = data.sort_preference
    db.commit()
    db.refresh(pref)
    return pref
