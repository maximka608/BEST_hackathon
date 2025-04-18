# BEST_hackaton

### ♿ Inclusive Map API

FastAPI application for storing objects, commenting, and building accessible routes for people with reduced mobility (PRM) using OpenStreetMap data.

 ---

### ✅ Features
✔ Filter places by categories, such as convenience for visually impaired people or wheelchair accessibility, based on various factors like ramps, tactile elements, convenient entrances, accessible toilets, etc.

✔ Build an optimal route, considering inclusivity filters.

✔ Add reviews — the ability to rate places and leave comments.

✔ Regular users can suggest changes to the accessibility features.

✔ Ability to add users with special needs.

✔ Users with special needs have access to edit the accessibility features.

✔ Responsive design

✔ User-friendly and intuitive design


---
### Setup Database

run init_db.py to create your DB

run following command to init alembic:

```python
alembic init alembic
```

in alembic/env.py set your target_metadata as follows:
```python
from src.models import Base
target_metadata = Base.metadata
```

in alembic.ini change the connection string to your DB(run config.py to get your link)
```ini
sqlalchemy.url = sqlite:////...ACTUAL_LINK_TO_YOUR_DB
```

to create migrations run:
```python
alembic revision --autogenerate -m "Create tables"
```

to apply migrations run:
```python
alembic upgrade head
```

---

### 🛠 Tech Stack
FastAPI — for creating REST APIs.

SQLLite + SQLAlchemy — for storing objects and comments.

MongoDB — for OpenStreetMap geodata.

NetworkX — for building graphs and implementing the A* algorithm.

Pydantic — for validation and serialization.

---

### 🔧 Project Configuration
The project uses environment variables to configure the database connection, authorization parameters, and CORS policy. A .env file is used to store sensitive information and should be created in the root directory of the project.

⚙️ Key Configuration Parameters:
MONGODB_URL – the connection string for MongoDB. If not provided, it defaults to mongo_url.

MONGO_DB_NAME – the name of the MongoDB database (hackathon_lviv).

DATABASE_URL – the path to a local SQLite database. It is automatically generated based on the location of the object.db file in the project's root directory.

SECRET_KEY – the secret key used for signing JWT tokens.

ALGORITHM – the algorithm used for JWT encryption (e.g., HS256).

ACCESS_TOKEN_EXPIRE_MINUTES – the lifetime of the access token in minutes (defaults to 120 minutes).

REFRESH_TOKEN_EXPIRE_DAYS – the lifetime of the refresh token in days (defaults to 30 days).

origins – the list of allowed CORS origins from which the API can be accessed. For example, http://localhost:3000 is used for frontend development.

---

### 🔗 Main Routes

### 🔹 `/comments`

#### `POST /comments`
Add a new comment or rating to an object.

**Input Data (JSON):**
```json
{
  "object_id": "str",
  "text": "Optional[str]",
  "rating": "Optional[int]"
}
```

### 🔹 `/comments/{object_id}` 
Get a list of comments for an object.
Returns an array of comments or a message "No comments found".

### 🔹 `/ratings/{object_id} `
Get only the ratings for an object.
Returns an array of RatingResponse objects.


### 🔹 `/find_path`
Find a route between two points using the A* algorithm.

**Input Data (JSON):**
```json
{
  "start": {"lat": float, "lon": float},
  "end": {"lat": float, "lon": float},
  "accessible": true | false
}
```
If accessible=true, the route considers restrictions for PRM: wheelchair, incline, kerb, surface, etc.
Returns a list of route coordinates or a message if no path is found.

--- 

### ⚙️ A Pathfinding Algorithm*
- haversine(): calculates the distance between two coordinates.

 - calculate_accessibility_weight(): calculates the "difficulty" of the route for people with reduced mobility.

- build_graph(): creates a graph with weighted edges.

- astar_path(): finds the shortest (or most accessible) route

---

### 🔐 Authentication & Authorization
- The application includes a robust authentication and authorization system to manage users, roles, and secure access to API endpoints.

#### User Registration and Login
- Sign Up: New users can create an account by providing a unique email and username. The system ensures that each email and username is not already registered.

- Sign In: Registered users can log in using their email and password. Upon successful authentication, the system issues an access token and a refresh token using JWT (JSON Web Tokens).

- Logout: Users can invalidate their tokens to securely log out from the system.

#### Token Management
- Access Tokens: Short-lived tokens used for authenticating user requests.

- Refresh Tokens: Long-lived tokens used to renew access tokens without requiring re-authentication.

- Tokens are stored and managed in the database to support secure logout and token revocation.

####  Role-Based Access Control (RBAC)
The system distinguishes between regular users and administrators.
- Promote regular users to admin status.
- Demote admins back to regular user roles.
- Promotion and demotion actions are protected and accessible only by authenticated administrators.

####  User Profile Management

- View their profile details.
- Delete their own account.


####  Security Highlights
- Passwords are securely hashed before storage.

-  All endpoints requiring authentication validate access tokens using JWT.

-  Sensitive admin routes are protected using custom dependencies that ensure the caller has admin privileges.
