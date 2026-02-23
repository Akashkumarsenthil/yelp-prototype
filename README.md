# Yelp Prototype - Restaurant Discovery & Review Platform

A full-stack Yelp-style restaurant discovery and review platform with an AI-powered recommendation chatbot.

**Course:** DATA 236 | **Lab 1** | Spring 2026

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 19, Vite 7, TailwindCSS v4, React Router v7, Axios |
| **Backend** | Python 3.11+, FastAPI, SQLAlchemy ORM, PyMySQL |
| **Database** | MySQL 8.0+ |
| **AI Assistant** | LangChain, OpenAI GPT-4o-mini, Tavily Web Search |
| **Authentication** | JWT (python-jose) + bcrypt password hashing |

---

## Features

### User (Reviewer)
- **Signup / Login / Logout** with JWT authentication and bcrypt-hashed passwords
- **Profile Management** - update name, phone, about me, city, state, country (dropdown), languages, gender; upload profile picture
- **AI Preferences** - set cuisine, price range, dietary needs, ambiance, location, and sort preferences for the AI chatbot
- **Restaurant Search / Dashboard** - search by name, cuisine, keywords, city/zip; filter by cuisine type and price range
- **Restaurant Details** - view name, cuisine, address, description, hours, contact, photos, average rating, reviews
- **Add Restaurant Listing** - create new restaurant entries with full details
- **Reviews** - add, edit, delete own reviews with 1-5 star ratings and comments
- **Favourites** - mark/unmark restaurants as favourites; dedicated favourites tab
- **History** - view past reviews and restaurants added
- **AI Chatbot** - conversational restaurant recommendations on the home screen

### Restaurant Owner
- **Owner Signup** with restaurant location
- **Restaurant Profile Management** - edit details, upload photos, manage hours
- **Claim Restaurant** - claim existing unclaimed restaurant listings
- **View Reviews** - read-only access to all reviews for owned restaurants
- **Analytics Dashboard** - total restaurants, total reviews, overall rating, rating distribution bar charts, recent reviews

### AI Assistant Chatbot
- Prominently displayed floating chat widget on home screen
- Fetches user's saved preferences for personalization
- Natural language query interpretation via LangChain + OpenAI
- Searches and ranks restaurants from the database
- Multi-turn conversation with follow-up support
- Quick action buttons: "Find dinner tonight", "Best rated near me", "Vegan options"
- Clickable restaurant cards linking to full detail pages

---

## Prerequisites

Before running the app, make sure you have these installed:

| Tool | Version | Check Command |
|------|---------|---------------|
| **Python** | 3.11+ | `python3 --version` |
| **Node.js** | 18+ | `node --version` |
| **npm** | 9+ | `npm --version` |
| **MySQL** | 8.0+ | `mysql --version` |
| **Git** | Any | `git --version` |

You will also need:
- An **OpenAI API key** (for the AI chatbot) - get one at https://platform.openai.com/api-keys
- A **Tavily API key** (for web search in chatbot) - get one at https://www.tavily.com

---

## Local Setup - Step by Step

### Step 1: Clone the Repository

```bash
git clone https://github.com/<your-username>/yelp-prototype.git
cd yelp-prototype
```

### Step 2: Set Up MySQL Database

Open a MySQL shell and run:

```sql
CREATE DATABASE IF NOT EXISTS yelp_db;
```

Or use the provided script:

```bash
mysql -u root -p < backend/init_db.sql
```

> **Note:** The application tables are auto-created by SQLAlchemy when the backend starts for the first time.

### Step 3: Set Up the Backend

```bash
cd backend

# Create a Python virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate          # Windows

# Install Python dependencies
pip install -r requirements.txt

# Create your .env file
cp .env.example .env
```

Now open `backend/.env` and fill in your actual values:

```env
DATABASE_URL=mysql+pymysql://root:YOUR_MYSQL_PASSWORD@localhost:3306/yelp_db
SECRET_KEY=pick-a-random-secret-string-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxxxxxxxxxx
```

Start the backend server:

```bash
uvicorn app.main:app --reload --port 8000
```

You should see:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Verify it works by visiting: http://localhost:8000/docs (Swagger UI)

### Step 4: Set Up the Frontend

Open a **new terminal** (keep the backend running):

```bash
cd frontend

# Install Node.js dependencies
npm install

# Start the development server
npm run dev
```

You should see:

```
  VITE v7.x.x  ready in Xms

  ➜  Local:   http://localhost:5173/
```

### Step 5: Open the App

Open http://localhost:5173 in your browser. You're ready to go!

---

## Running the App (After Initial Setup)

Every time you want to run the app after the initial setup:

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

---

## API Documentation

FastAPI auto-generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/signup` | User / Owner registration |
| POST | `/api/auth/login` | Login (returns JWT token) |
| GET | `/api/users/me` | Get current user profile |
| PUT | `/api/users/me` | Update profile information |
| POST | `/api/users/me/picture` | Upload profile picture |
| GET | `/api/preferences/` | Get AI preferences |
| PUT | `/api/preferences/` | Update AI preferences |
| GET | `/api/restaurants/` | Search / list restaurants |
| POST | `/api/restaurants/` | Create a new restaurant |
| GET | `/api/restaurants/{id}` | Get restaurant details |
| PUT | `/api/restaurants/{id}` | Update restaurant |
| POST | `/api/restaurants/{id}/claim` | Claim restaurant (owner) |
| POST | `/api/restaurants/{id}/photos` | Upload restaurant photo |
| POST | `/api/reviews/` | Create a review |
| GET | `/api/reviews/restaurant/{id}` | Get reviews for a restaurant |
| PUT | `/api/reviews/{id}` | Update own review |
| DELETE | `/api/reviews/{id}` | Delete own review |
| GET | `/api/reviews/user/me` | Get my reviews |
| GET | `/api/favourites/` | List favourite restaurants |
| POST | `/api/favourites/{id}` | Add to favourites |
| DELETE | `/api/favourites/{id}` | Remove from favourites |
| GET | `/api/history/` | User activity history |
| POST | `/api/ai-assistant/chat` | AI chatbot conversation |
| GET | `/api/owner/dashboard` | Owner analytics dashboard |
| GET | `/api/owner/restaurants` | Owner's restaurants |
| GET | `/api/owner/restaurants/{id}/reviews` | Reviews for owned restaurant |

---

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | MySQL connection string | `mysql+pymysql://root:pass@localhost:3306/yelp_db` |
| `SECRET_KEY` | JWT signing secret (any random string) | `my-super-secret-key-123` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry in minutes | `60` |
| `OPENAI_API_KEY` | OpenAI API key for chatbot | `sk-...` |
| `TAVILY_API_KEY` | Tavily API key for web search | `tvly-...` |

---

## Project Structure

```
LAB1/
├── backend/
│   ├── app/
│   │   ├── main.py                # FastAPI app entry point + CORS + routes
│   │   ├── config.py              # Pydantic settings (env vars)
│   │   ├── database.py            # SQLAlchemy engine + session
│   │   ├── models/                # SQLAlchemy ORM models
│   │   │   ├── user.py            # User model (reviewer + owner)
│   │   │   ├── restaurant.py      # Restaurant model
│   │   │   ├── review.py          # Review model
│   │   │   ├── favourite.py       # Favourite model
│   │   │   ├── preference.py      # User AI preferences model
│   │   │   └── restaurant_photo.py
│   │   ├── schemas/               # Pydantic request/response schemas
│   │   │   ├── user.py
│   │   │   ├── restaurant.py
│   │   │   ├── review.py
│   │   │   └── preference.py
│   │   ├── routers/               # API route handlers
│   │   │   ├── auth.py            # Signup / Login
│   │   │   ├── users.py           # Profile management
│   │   │   ├── preferences.py     # AI preferences CRUD
│   │   │   ├── restaurants.py     # Restaurant CRUD + search
│   │   │   ├── reviews.py         # Review CRUD
│   │   │   ├── favourites.py      # Favourites management
│   │   │   ├── owner.py           # Owner dashboard + analytics
│   │   │   ├── ai_assistant.py    # AI chatbot endpoint
│   │   │   └── history.py         # User activity history
│   │   ├── services/
│   │   │   └── ai_assistant.py    # LangChain + OpenAI chatbot logic
│   │   └── utils/
│   │       └── auth.py            # JWT + bcrypt utilities
│   ├── init_db.sql                # Database initialization script
│   ├── requirements.txt           # Python dependencies
│   └── .env.example               # Environment variable template
├── frontend/
│   ├── src/
│   │   ├── main.jsx               # React entry point (BrowserRouter + AuthProvider)
│   │   ├── App.jsx                # Route definitions
│   │   ├── index.css              # TailwindCSS import
│   │   ├── components/
│   │   │   ├── Navbar.jsx         # Responsive navigation bar
│   │   │   ├── RestaurantCard.jsx # Restaurant display card
│   │   │   ├── StarRating.jsx     # Interactive star rating
│   │   │   ├── ChatBot.jsx        # AI chatbot floating widget
│   │   │   └── ProtectedRoute.jsx # Auth route guard
│   │   ├── pages/
│   │   │   ├── auth/
│   │   │   │   ├── Login.jsx
│   │   │   │   └── Signup.jsx
│   │   │   ├── user/
│   │   │   │   ├── Profile.jsx
│   │   │   │   ├── Preferences.jsx
│   │   │   │   ├── Favourites.jsx
│   │   │   │   └── History.jsx
│   │   │   ├── restaurant/
│   │   │   │   ├── Explore.jsx        # Home / search dashboard
│   │   │   │   ├── RestaurantDetail.jsx
│   │   │   │   └── AddRestaurant.jsx
│   │   │   └── owner/
│   │   │       ├── OwnerDashboard.jsx
│   │   │       ├── ManageRestaurant.jsx
│   │   │       └── OwnerReviews.jsx
│   │   ├── context/
│   │   │   └── AuthContext.jsx    # Auth state management
│   │   └── services/
│   │       └── api.js             # Axios API service layer
│   ├── package.json
│   └── vite.config.js             # Vite + Tailwind + proxy config
├── .gitignore
└── README.md
```

---

## Uploading to GitHub

See the step-by-step instructions provided separately.

---

## Troubleshooting

| Issue | Solution |
|-------|---------|
| `ModuleNotFoundError` in backend | Make sure venv is activated: `source venv/bin/activate` |
| MySQL connection refused | Ensure MySQL is running: `brew services start mysql` (macOS) |
| `Access denied for user 'root'` | Check your MySQL password in `.env` matches your actual root password |
| Frontend can't reach backend | Make sure backend is running on port 8000; Vite proxy handles `/api` |
| AI chatbot returns errors | Verify your `OPENAI_API_KEY` is valid and has credits |
| Port already in use | Kill existing process: `lsof -ti:8000 \| xargs kill` or use a different port |
