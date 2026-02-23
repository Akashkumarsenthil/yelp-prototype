from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.database import engine, Base
from app.routers import auth, users, preferences, restaurants, reviews, favourites, owner, ai_assistant, history

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Yelp Prototype API",
    description="A Yelp-style restaurant discovery and review platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads/profiles", exist_ok=True)
os.makedirs("uploads/restaurants", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(preferences.router)
app.include_router(restaurants.router)
app.include_router(reviews.router)
app.include_router(favourites.router)
app.include_router(owner.router)
app.include_router(ai_assistant.router)
app.include_router(history.router)


@app.get("/")
def root():
    return {"message": "Yelp Prototype API", "docs": "/docs"}
