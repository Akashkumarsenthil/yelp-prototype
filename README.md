# Yelp Prototype - Restaurant Discovery & Review Platform

A full-stack Yelp-style restaurant discovery and review platform with an AI-powered recommendation chatbot.

**Course:** DATA 236 | **Lab 1** | Spring 2026

**Repository:** https://github.com/Akashkumarsenthil/yelp-prototype

---

## Tech Stack

### Backend
| Package | Version | Purpose |
|---------|---------|---------|
| Python | 3.9.6 | Runtime |
| FastAPI | 0.115.6 | Web framework (REST API) |
| Uvicorn | 0.34.0 | ASGI server |
| SQLAlchemy | 2.0.36 | ORM (database models & queries) |
| PyMySQL | 1.1.1 | MySQL database driver |
| Pydantic | 2.10.4 | Request/response validation |
| Pydantic-Settings | 2.7.1 | Environment variable management |
| python-jose | 3.3.0 | JWT token creation & verification |
| passlib + bcrypt | 1.7.4 / 4.2.1 | Password hashing (bcrypt) |
| python-multipart | 0.0.18 | File upload handling |
| LangChain | 0.3.14 | AI chatbot framework |
| LangChain-OpenAI | 0.3.0 | OpenAI integration for LangChain |
| LangChain-Community | 0.3.14 | Community integrations |
| tavily-python | 0.5.0 | Tavily web search for AI chatbot |
| python-dotenv | 1.0.1 | Load .env file variables |
| Pillow | 11.1.0 | Image processing |
| aiofiles | 24.1.0 | Async file operations |
| cryptography | 44.0.0 | Cryptographic operations for JWT |

### Frontend
| Package | Version | Purpose |
|---------|---------|---------|
| Node.js | 23.7.0 | Runtime |
| npm | 10.9.2 | Package manager |
| React | 19.2.0 | UI framework |
| React DOM | 19.2.0 | React rendering |
| Vite | 7.3.1 | Build tool & dev server |
| TailwindCSS | 4.2.0 | Utility-first CSS framework |
| React Router DOM | 7.13.0 | Client-side routing |
| Axios | 1.13.5 | HTTP client for API calls |
| React Icons | 5.5.0 | Icon library |
| React Hot Toast | 2.6.0 | Toast notifications |
| ESLint | 9.39.1 | Code linting |

### Database
| Tool | Version | Purpose |
|------|---------|---------|
| MySQL | 9.6.0 (Homebrew) | Relational database |

### External APIs
| Service | Purpose | Get Key At |
|---------|---------|------------|
| OpenAI (GPT-4o-mini) | AI chatbot natural language understanding | https://platform.openai.com/api-keys |
| Tavily | Web search for restaurant context in chatbot | https://www.tavily.com |

---

## Features

### User (Reviewer)
- **Signup / Login / Logout** — JWT authentication with bcrypt-hashed passwords
- **Profile Management** — update name, phone, about me, city, state, country (dropdown), languages, gender; upload profile picture
- **AI Preferences** — set cuisine, price range, dietary needs, ambiance, location, and sort preferences for the AI chatbot
- **Restaurant Search / Dashboard** — search by name, cuisine, keywords, city/zip; filter by cuisine type and price range
- **Restaurant Details** — view name, cuisine, address, description, hours, contact, photos, average rating, reviews
- **Add Restaurant Listing** — create new restaurant entries with full details
- **Reviews** — add, edit, delete own reviews with 1–5 star ratings and comments
- **Favourites** — mark/unmark restaurants as favourites; dedicated favourites tab
- **History** — view past reviews and restaurants added
- **AI Chatbot** — conversational restaurant recommendations on the home screen

### Restaurant Owner
- **Owner Signup** with restaurant location
- **Restaurant Profile Management** — edit details, upload photos, manage hours
- **Claim Restaurant** — claim existing unclaimed restaurant listings
- **View Reviews** — read-only access to all reviews for owned restaurants
- **Analytics Dashboard** — total restaurants, total reviews, overall rating, rating distribution bar charts, recent reviews

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

Make sure you have these installed before setting up:

| Tool | Required | Install Command (macOS) | Check Command |
|------|----------|------------------------|---------------|
| **Homebrew** | Yes | `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"` | `brew --version` |
| **Python 3** | 3.9+ | Comes with macOS (or `brew install python`) | `python3 --version` |
| **Node.js** | 18+ | `brew install node` | `node --version` |
| **npm** | 9+ | Comes with Node.js | `npm --version` |
| **MySQL** | 8.0+ | `brew install mysql` | `mysql --version` |
| **Git** | Any | `brew install git` | `git --version` |

---

## Installation & Setup (Step by Step)

### Step 1: Install MySQL (if not already installed)

```bash
# Install MySQL via Homebrew
brew install mysql

# Start MySQL as a background service
brew services start mysql

# Secure the installation (set root password, remove test data)
mysql_secure_installation
```

During `mysql_secure_installation`:
- **Set a root password** (remember this — you'll need it for the `.env` file)
- Remove anonymous users → **Y**
- Disallow root login remotely → **Y**
- Remove test database → **Y**
- Reload privilege tables → **Y**

### Step 2: Create the Database

```bash
mysql -u root -p
```

Enter your root password, then run:

```sql
CREATE DATABASE IF NOT EXISTS yelp_db;
exit;
```

### Step 3: Clone the Repository

```bash
git clone https://github.com/Akashkumarsenthil/yelp-prototype.git
cd yelp-prototype
```

### Step 4: Set Up the Backend

```bash
cd backend

# Create a Python virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate          # Windows

# Install all Python dependencies
pip install -r requirements.txt

# Create your .env file from the template
cp .env.example .env
```

Now open `backend/.env` and fill in your actual values:

```env
DATABASE_URL=mysql+pymysql://root:YOUR_MYSQL_PASSWORD@localhost:3306/yelp_db
SECRET_KEY=pick-any-random-string-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxxxxxxxxxx
```

> **Important:** If your MySQL password contains special characters like `#`, `@`, or `%`, they must be URL-encoded in the connection string. For example:
> - `#` → `%23`
> - `@` → `%40`
> - `%` → `%25`
>
> Example: password `Akash#123` becomes `Akash%23123` in the URL.

Start the backend server:

```bash
uvicorn app.main:app --reload --port 8000
```

You should see:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

> SQLAlchemy auto-creates all database tables on the first startup.

Verify the API is working: http://localhost:8000/docs (Swagger UI)

### Step 5: Set Up the Frontend

Open a **new terminal** (keep the backend running in the first one):

```bash
cd frontend

# Install all Node.js dependencies
npm install

# Start the Vite development server
npm run dev
```

You should see:

```
  VITE v7.3.1  ready in Xms

  ➜  Local:   http://localhost:5173/
```

### Step 6: Open the App

Open **http://localhost:5173** in your browser. The app is ready!

---

## Running the App (After Initial Setup)

You need **two terminals** running simultaneously:

**Terminal 1 — Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 — Frontend:**
```bash
cd frontend
npm run dev
```

Make sure MySQL is running:
```bash
brew services start mysql
```

---

## API Documentation

FastAPI auto-generates interactive API documentation:

- **Swagger UI:** http://localhost:8000/docs (test APIs directly in the browser)
- **ReDoc:** http://localhost:8000/redoc (alternative read-only docs)

### API Endpoints

#### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/signup` | Register a new user or owner |
| POST | `/api/auth/login` | Login and receive JWT token |

#### User Profile
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users/me` | Get current user profile |
| PUT | `/api/users/me` | Update profile information |
| POST | `/api/users/me/picture` | Upload profile picture |

#### User Preferences (for AI Assistant)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/preferences/` | Get saved AI preferences |
| PUT | `/api/preferences/` | Update AI preferences |

#### Restaurants
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/restaurants/` | Search/list restaurants (query params: name, cuisine_type, keywords, city, zip_code) |
| POST | `/api/restaurants/` | Create a new restaurant |
| GET | `/api/restaurants/{id}` | Get restaurant details |
| PUT | `/api/restaurants/{id}` | Update restaurant (owner/creator only) |
| POST | `/api/restaurants/{id}/claim` | Claim an unclaimed restaurant (owner only) |
| POST | `/api/restaurants/{id}/photos` | Upload a restaurant photo |

#### Reviews
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/reviews/` | Create a review (rating 1–5 + comment) |
| GET | `/api/reviews/restaurant/{id}` | Get all reviews for a restaurant |
| GET | `/api/reviews/user/me` | Get current user's reviews |
| PUT | `/api/reviews/{id}` | Update own review |
| DELETE | `/api/reviews/{id}` | Delete own review |

#### Favourites
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/favourites/` | List favourite restaurants |
| POST | `/api/favourites/{id}` | Add restaurant to favourites |
| DELETE | `/api/favourites/{id}` | Remove from favourites |
| GET | `/api/favourites/check/{id}` | Check if restaurant is favourited |

#### History
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/history/` | Get user activity history (reviews + restaurants added) |

#### AI Assistant
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/ai-assistant/chat` | Send message to AI chatbot (input: message + conversation_history) |

#### Owner Dashboard
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/owner/dashboard` | Get analytics (total restaurants, reviews, ratings, distributions) |
| GET | `/api/owner/restaurants` | List owner's restaurants |
| GET | `/api/owner/restaurants/{id}/reviews` | Get reviews for an owned restaurant |

---

## Environment Variables

Stored in `backend/.env` (never committed to git):

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | MySQL connection string | `mysql+pymysql://root:pass@localhost:3306/yelp_db` |
| `SECRET_KEY` | JWT signing secret (any random string) | `my-super-secret-key-123` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry in minutes | `60` |
| `OPENAI_API_KEY` | OpenAI API key for AI chatbot | `sk-...` |
| `TAVILY_API_KEY` | Tavily API key for web search | `tvly-...` |

---

## Project Structure

```
yelp-prototype/
├── backend/
│   ├── app/
│   │   ├── main.py                # FastAPI app entry point, CORS, route registration
│   │   ├── config.py              # Pydantic settings (loads .env)
│   │   ├── database.py            # SQLAlchemy engine, session, Base
│   │   ├── models/                # SQLAlchemy ORM models
│   │   │   ├── user.py            # User model (reviewer + owner roles)
│   │   │   ├── restaurant.py      # Restaurant model
│   │   │   ├── review.py          # Review model (1–5 stars + comment)
│   │   │   ├── favourite.py       # User-Restaurant favourite mapping
│   │   │   ├── preference.py      # User AI preferences (cuisine, diet, etc.)
│   │   │   └── restaurant_photo.py # Restaurant photo URLs
│   │   ├── schemas/               # Pydantic request/response schemas
│   │   │   ├── user.py            # UserSignup, UserLogin, UserOut, Token
│   │   │   ├── restaurant.py      # RestaurantCreate, RestaurantOut, RestaurantSearch
│   │   │   ├── review.py          # ReviewCreate, ReviewUpdate, ReviewOut
│   │   │   └── preference.py      # PreferenceUpdate, PreferenceOut, ChatMessage
│   │   ├── routers/               # API route handlers (one per feature)
│   │   │   ├── auth.py            # POST /signup, /login
│   │   │   ├── users.py           # GET/PUT /users/me, POST /users/me/picture
│   │   │   ├── preferences.py     # GET/PUT /preferences
│   │   │   ├── restaurants.py     # CRUD + search + claim + photo upload
│   │   │   ├── reviews.py         # CRUD for reviews + rating recalculation
│   │   │   ├── favourites.py      # Add/remove/list/check favourites
│   │   │   ├── owner.py           # Owner dashboard + analytics
│   │   │   ├── ai_assistant.py    # POST /ai-assistant/chat
│   │   │   └── history.py         # GET /history (reviews + restaurants added)
│   │   ├── services/
│   │   │   └── ai_assistant.py    # LangChain + OpenAI chatbot logic
│   │   └── utils/
│   │       └── auth.py            # hash_password, verify_password, create_access_token, get_current_user
│   ├── init_db.sql                # SQL script to create yelp_db database
│   ├── requirements.txt           # All Python dependencies with pinned versions
│   └── .env.example               # Template for environment variables
├── frontend/
│   ├── src/
│   │   ├── main.jsx               # Entry point: BrowserRouter + AuthProvider + App
│   │   ├── App.jsx                # All route definitions + Navbar + ChatBot
│   │   ├── index.css              # TailwindCSS v4 import
│   │   ├── components/
│   │   │   ├── Navbar.jsx         # Red/white responsive nav, profile dropdown, mobile menu
│   │   │   ├── RestaurantCard.jsx # Card component (grid + list + compact variants)
│   │   │   ├── StarRating.jsx     # Interactive/display star rating (1–5)
│   │   │   ├── ChatBot.jsx        # Floating AI chat widget, quick actions, restaurant cards
│   │   │   └── ProtectedRoute.jsx # Redirects to /login if not authenticated
│   │   ├── pages/
│   │   │   ├── auth/
│   │   │   │   ├── Login.jsx      # Email + password login form
│   │   │   │   └── Signup.jsx     # Registration with role selection (user/owner)
│   │   │   ├── user/
│   │   │   │   ├── Profile.jsx    # Profile editor + picture upload
│   │   │   │   ├── Preferences.jsx # AI preference checkboxes, radios, dropdowns
│   │   │   │   ├── Favourites.jsx # Grid of favourite restaurants with remove button
│   │   │   │   └── History.jsx    # Timeline of reviews and restaurants added
│   │   │   ├── restaurant/
│   │   │   │   ├── Explore.jsx    # Home page: hero search bar, filters, restaurant grid
│   │   │   │   ├── RestaurantDetail.jsx # Full detail view, reviews, write review, favourite
│   │   │   │   └── AddRestaurant.jsx    # Multi-section form to create a restaurant
│   │   │   └── owner/
│   │   │       ├── OwnerDashboard.jsx   # Summary cards, rating distributions, recent reviews
│   │   │       ├── ManageRestaurant.jsx # Inline edit form for owned restaurants
│   │   │       └── OwnerReviews.jsx     # Read-only reviews with filter/sort
│   │   ├── context/
│   │   │   └── AuthContext.jsx    # React context: user, token, login, logout, updateUser
│   │   └── services/
│   │       └── api.js             # Axios instance + all API functions (auth, user, restaurant, review, favourite, owner, chat, history)
│   ├── package.json               # Node.js dependencies
│   └── vite.config.js             # Vite config: React plugin, TailwindCSS plugin, API proxy to :8000
├── .gitignore                     # Excludes venv, node_modules, .env, uploads, __pycache__
└── README.md
```

---

## System Design

```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│   Browser    │  HTTP   │   Vite Dev   │  Proxy   │   FastAPI    │
│   React UI   │◄───────►│   Server     │◄────────►│   Backend    │
│  :5173       │         │   :5173      │  /api/*  │   :8000      │
└──────────────┘         └──────────────┘         └──────┬───────┘
                                                         │
                                          ┌──────────────┼──────────────┐
                                          │              │              │
                                    ┌─────▼─────┐ ┌─────▼─────┐ ┌─────▼─────┐
                                    │   MySQL   │ │  OpenAI   │ │  Tavily   │
                                    │  yelp_db  │ │  GPT-4o   │ │  Search   │
                                    │  :3306    │ │  -mini    │ │   API     │
                                    └───────────┘ └───────────┘ └───────────┘
```

- **React** frontend runs on Vite dev server (port 5173)
- **Vite** proxies all `/api/*` and `/uploads/*` requests to the FastAPI backend (port 8000)
- **FastAPI** handles all business logic, auth, and database operations
- **SQLAlchemy** ORM manages MySQL through PyMySQL driver
- **LangChain** + **OpenAI** power the AI chatbot; **Tavily** provides supplementary web search

---

## Troubleshooting

| Issue | Solution |
|-------|---------|
| `ModuleNotFoundError` in backend | Make sure venv is activated: `source backend/venv/bin/activate` |
| `Access denied for user 'root'` | Your MySQL password in `.env` is wrong. Check it, and URL-encode special chars (`#` → `%23`) |
| MySQL connection refused | Make sure MySQL is running: `brew services start mysql` |
| `[Errno 48] Address already in use` | Kill the old process: `lsof -ti:8000 \| xargs kill -9` |
| Frontend can't reach backend | Backend must be running on port 8000. Vite proxy in `vite.config.js` handles routing |
| AI chatbot returns errors | Check that `OPENAI_API_KEY` in `.env` is valid and has credits |
| `NotOpenSSLWarning` on startup | Harmless warning about system SSL — does not affect the app |
| Tables not showing in MySQL | Start the backend once — SQLAlchemy auto-creates them on first run |
| Password has special characters | URL-encode them in `DATABASE_URL`: `#` → `%23`, `@` → `%40`, `%` → `%25` |

---

## Git Repository Guidelines

- **Private repository** — collaborators invited: `Devdatta1999`, `Saurabh2504`
- **Commit history** — meaningful commit messages describing changes
- **No venv or __pycache__** committed — handled by `.gitignore`
- **No .env** committed — secrets stay local; `.env.example` provided as template
- **requirements.txt** included with pinned versions for reproducible installs
