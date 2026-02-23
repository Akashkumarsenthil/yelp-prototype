import json
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from app.config import get_settings
from app.models.restaurant import Restaurant
from app.models.preference import UserPreference

settings = get_settings()


def _load_preferences(db: Session, user_id: int) -> dict:
    pref = db.query(UserPreference).filter(UserPreference.user_id == user_id).first()
    if not pref:
        return {}
    result = {}
    if pref.cuisine_preferences:
        try:
            result["cuisine_preferences"] = json.loads(pref.cuisine_preferences)
        except json.JSONDecodeError:
            result["cuisine_preferences"] = [pref.cuisine_preferences]
    if pref.price_range:
        result["price_range"] = pref.price_range
    if pref.preferred_locations:
        try:
            result["preferred_locations"] = json.loads(pref.preferred_locations)
        except json.JSONDecodeError:
            result["preferred_locations"] = [pref.preferred_locations]
    if pref.dietary_needs:
        try:
            result["dietary_needs"] = json.loads(pref.dietary_needs)
        except json.JSONDecodeError:
            result["dietary_needs"] = [pref.dietary_needs]
    if pref.ambiance_preferences:
        try:
            result["ambiance_preferences"] = json.loads(pref.ambiance_preferences)
        except json.JSONDecodeError:
            result["ambiance_preferences"] = [pref.ambiance_preferences]
    if pref.sort_preference:
        result["sort_preference"] = pref.sort_preference
    return result


def _search_restaurants(db: Session, filters: dict, limit: int = 10) -> List[dict]:
    query = db.query(Restaurant)

    cuisine = filters.get("cuisine")
    if cuisine:
        query = query.filter(Restaurant.cuisine_type.ilike(f"%{cuisine}%"))

    price = filters.get("price_range")
    if price:
        query = query.filter(Restaurant.pricing_tier == price)

    city = filters.get("city")
    if city:
        query = query.filter(Restaurant.city.ilike(f"%{city}%"))

    ambiance = filters.get("ambiance")
    if ambiance:
        query = query.filter(Restaurant.ambiance.ilike(f"%{ambiance}%"))

    keywords = filters.get("keywords")
    if keywords:
        kw = f"%{keywords}%"
        query = query.filter(
            or_(
                Restaurant.description.ilike(kw),
                Restaurant.amenities.ilike(kw),
                Restaurant.name.ilike(kw),
            )
        )

    query = query.order_by(Restaurant.average_rating.desc())
    restaurants = query.limit(limit).all()
    return [
        {
            "id": r.id, "name": r.name, "cuisine_type": r.cuisine_type,
            "city": r.city, "pricing_tier": r.pricing_tier,
            "average_rating": r.average_rating, "review_count": r.review_count,
            "description": r.description, "ambiance": r.ambiance,
            "address": r.address,
        }
        for r in restaurants
    ]


def get_ai_response(db: Session, user_id: int, message: str, conversation_history: list) -> dict:
    preferences = _load_preferences(db, user_id)

    all_restaurants = _search_restaurants(db, {}, limit=50)

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=settings.OPENAI_API_KEY,
        temperature=0.7,
    )

    system_prompt = f"""You are a helpful restaurant recommendation assistant for a Yelp-like platform.
You help users discover restaurants based on their preferences and queries.

User Preferences: {json.dumps(preferences) if preferences else "No preferences saved yet."}

Available Restaurants in the database:
{json.dumps(all_restaurants, indent=2)}

Instructions:
- Use the user's saved preferences to personalize recommendations.
- When recommending restaurants, include the restaurant name, rating (stars), price tier, and a brief reason for the recommendation.
- If the user asks about specific cuisines, dietary needs, or ambiance, filter accordingly.
- Be conversational and helpful, not robotic.
- If no restaurants match, suggest the closest alternatives and explain why.
- Support follow-up questions and refine recommendations.
- Format restaurant recommendations as numbered lists with key details.
- Always reference the restaurant ID so the frontend can link to the detail page.
- Respond with JSON in this format:
{{
  "response": "Your conversational response text here",
  "restaurant_ids": [list of recommended restaurant IDs]
}}
"""

    messages = [SystemMessage(content=system_prompt)]

    for msg in conversation_history:
        if msg.get("role") == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg.get("role") == "assistant":
            messages.append(AIMessage(content=msg["content"]))

    messages.append(HumanMessage(content=message))

    try:
        response = llm.invoke(messages)
        content = response.content

        try:
            parsed = json.loads(content)
            response_text = parsed.get("response", content)
            rec_ids = parsed.get("restaurant_ids", [])
            recommended = [r for r in all_restaurants if r["id"] in rec_ids]
        except json.JSONDecodeError:
            response_text = content
            recommended = all_restaurants[:3] if all_restaurants else []

        return {"response": response_text, "restaurants": recommended}
    except Exception as e:
        return {
            "response": f"I'm sorry, I'm having trouble processing your request right now. Please try again later. (Error: {str(e)})",
            "restaurants": [],
        }
