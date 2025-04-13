# README for BEST_hackaton

## Project Overview

The BEST_hackaton project aims to develop an inclusive service for locating accessible venues based on various criteria, such as the presence of ramps, tactile elements, adapted toilets, etc. This service will enhance mobility and participation in community life for individuals with disabilities by providing a platform for users to evaluate locations, leave feedback, and filter venues based on accessibility features.

## Features

1. **Searchable Database**: Users can filter locations by categories (e.g., wheelchair accessibility, visual impairment accommodations).
2. **Route Optimization**: The system provides optimal route suggestions considering accessibility features.
3. **User Reviews**: Users can rate and leave comments on locations.
4. **Community Contributions**: Users can suggest changes to accessibility characteristics.
5. **Special User Accounts**: Users with disabilities can edit accessibility information.
6. **Automated Accessibility Rating**: The system automatically determines accessibility levels based on venue characteristics.

## Getting Started

### Prerequisites

- Python 3.x
- SQLite or another compatible database
- FastAPI
- Alembic

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your_username/BEST_hackaton.git
    cd BEST_hackaton
    ```

2. **Create the database**:
    Run the following script to initialize the database:
    ```bash
    python init_db.py
    ```

3. **Initialize Alembic**:
    To set up Alembic for database migrations, run:
    ```bash
    alembic init alembic
    ```

4. **Configure Alembic**:
    Edit `alembic/env.py` to set the target metadata:
    ```python
    from src.models import Base
    target_metadata = Base.metadata
    ```

5. **Set the Database Connection**:
    In `alembic.ini`, update the connection string:
    ```ini
    sqlalchemy.url = sqlite:////...ACTUAL_LINK_TO_YOUR_DB
    ```

6. **Create Migrations**:
    To generate migration files, execute:
    ```bash
    alembic revision --autogenerate -m "Create tables"
    ```

7. **Apply Migrations**:
    Run the following command to apply the migrations:
    ```bash
    alembic upgrade head
    ```

8. **Add Test Data**:
    Use the following script to populate the database with test data:
    ```bash
    python script_add_test_data.py
    ```

### API Documentation

The API is built using FastAPI and adheres to OpenAPI 3.1 specifications. Below are the key endpoints available:

#### Authentication

- **Sign Up**
    - **POST** `/api/auth/signup`
    - Register a new user.

- **Sign In**
    - **POST** `/api/auth/signin`
    - Authenticate an existing user.

- **Logout**
    - **PATCH** `/api/auth/logout`
    - Log out the user.

#### User Profile Management

- **Get User Profile**
    - **GET** `/api/user/`
    - Retrieve the user's profile information.

- **Delete User Account**
    - **DELETE** `/api/user/`
    - Allow user to delete their account.

#### Admin Functions

- **Promote User to Admin**
    - **PATCH** `/api/admin/promotion/{user_id}`
    - Make a user an admin.

- **Demote User from Admin**
    - **PATCH** `/api/admin/demotion/{user_id}`
    - Revoke admin privileges from a user.

---