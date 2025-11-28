# Gemini Project Context: airbnb-challenge-1 (Django Tweets App)

## Project Overview

This project is a Twitter-like application built with Django and Django REST Framework. It provides a RESTful API for managing users and tweets, including functionalities like creating tweets, listing tweets, user registration, login, and logout. The project uses `uv` for package management.

### Core Technologies

-   **Backend:** Django, Django REST Framework
-   **Package Manager:** uv
-   **Language:** Python

### Project Structure

The project is organized into three main Django apps:

-   `config`: The main project configuration, including `settings.py` and root `urls.py`.
-   `users`: Handles user management, authentication, and user-related API endpoints.
-   `tweets`: Manages tweet creation, retrieval, and other tweet-related functionalities.

## Building and Running

### 1. Install Dependencies

The project uses `uv` to manage dependencies, which are listed in `pyproject.toml`.

```bash
uv sync
```

### 2. Set Up the Database

Apply the database migrations to create the necessary tables.

```bash
uv run python manage.py migrate
```

### 3. Create a Superuser (Optional)

To access the Django admin interface, create a superuser.

```bash
uv run python manage.py createsuperuser
```

The admin panel is available at `/admin/`.

### 4. Run the Development Server

Start the Django development server.

```bash
uv run python manage.py runserver
```

The application will be accessible at `http://127.0.0.1:8000`.

### 5. Running Tests

The project includes a `test_api.py` file for testing the API. To run the tests, you can use the Django test runner:

```bash
uv run python manage.py test
```

## Development Conventions

### API Endpoints

The API is versioned under `/api/v1/`.

**User Endpoints (`/api/v1/users`)**

-   `GET /api/v1/users`: List all users (authentication required).
-   `POST /api/v1/users`: Create a new user (public).
-   `GET /api/v1/users/<pk>`: Retrieve a specific user's details.
-   `GET /api/v1/users/<pk>/tweets`: List tweets for a specific user.
-   `PUT /api/v1/users/password`: Update the authenticated user's password.
-   `POST /api/v1/users/login`: Log in a user and create a session.
-   `POST /api/v1/users/logout`: Log out the user.

**Tweet Endpoints (`/api/v1/tweets`)**

-   `GET /api/v1/tweets`: List all tweets.
-   `POST /api/v1/tweets`: Create a new tweet (authentication required).
-   `GET /api/v1/tweets/<pk>`: Retrieve a single tweet.
-   `PUT /api/v1/tweets/<pk>`: Update a tweet (only for the owner).
-   `DELETE /api/v1/tweets/<pk>`: Delete a tweet (only for the owner).

### Authentication

The API uses `SessionAuthentication`. Users need to log in via the `/api/v1/users/login` endpoint to obtain a session cookie for accessing protected endpoints.

### Data Models

-   **`User`**: The standard Django `User` model.
-   **`Tweet`**: Contains the tweet's content (`payload`) and a foreign key to the `User`.
-   **`Like`**: A through model for likes, linking a `User` and a `Tweet`.

### Serializers

The API relies on `djangorestframework.serializers.ModelSerializer` to convert Django models into JSON representations. Key serializers include `UserSerializer`, `TweetSerializer`, and serializers for handling login and password updates.
