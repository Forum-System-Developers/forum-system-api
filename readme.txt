<img src="forum.png" alt= "logo" width="100px"
style = "margin-top: 20px; margin-right: 500px"/>

---

# Forum System API

**WEB application for Telerik Academy**

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Endpoints](#endpoints)
- [Testing](#testing)
- [License](#license)

## Introduction
The **Forum System API** is a backend web application built using FastAPI for managing a forum-based discussion platform. It provides a RESTful API for user authentication, topic and reply management, category organization, and role-based permissions.

## Features
- **User Authentication & Authorization**: Supports secure login and role-based access.
- **Topic Management**: Create, read, update, and delete topics and replies.
- **Category Management**: Organize discussions in public and private categories.
- **Role-Based Access Control**: Restrict access based on user roles and permissions.
- **API Documentation**: Automatically generated Swagger documentation at `/docs`.

## Installation

To install and run the project locally, follow these steps:

### Prerequisites
- Python 3.12 or later
- [Poetry](https://python-poetry.org/) for dependency management

### Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/forum-system-api.git
   cd forum-system-api
   ```

2. **Install dependencies**:
   ```bash
   poetry install
   ```

3. **Set up environment variables**:
   Create a `.env` file with the following content:
   ```bash
    cp .env.example .env
   # Open .env and set the required configurations (e.g., database URL, JWT secret key)
   ```

4. **Run the application**:
   ```bash
   poetry run uvicorn main:app --reload
   ```

   The API will be available at `http://127.0.0.1:8000`.

## Usage

Once the application is running, you can access the interactive API documentation at:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

You can also use tools like Postman or `curl` to test the API endpoints.

## Project Structure

```plaintext
forum-system-api/
├── api/
│   └── api_v1/
│       └── routes/            # API route definitions
├── config.py                  # Configuration settings
├── main.py                    # Entry point of the application
├── persistence/
│   ├── database.py            # Database connection setup
│   └── models/                # SQLAlchemy ORM models
├── schemas/                   # Pydantic models for request/response schemas
├── services/                  # Core application logic and services
│   └── utils/                 # Utility functions for common tasks
├── pyproject.toml             # Project configuration and dependencies
├── README.md                  # Project documentation
└── tests/                     # Unit and integration tests
```

### Key Files and Directories
- **api/api_v1/routes/**: Contains FastAPI route definitions for different resources.
- **config.py**: Configuration file to manage environment-specific settings (e.g., database URLs).
- **persistence/database.py**: Sets up and manages the SQLAlchemy database connection.
- **persistence/models/**: SQLAlchemy ORM models that map to database tables.
- **schemas/**: Pydantic models for data validation and serialization.
- **services/**: Business logic for managing authentication, topics, categories, etc.
  - **utils/**: Utility functions to support core service logic.
- **tests/**: Unit tests and integration tests for various parts of the API.

## Configuration

The application uses environment variables for configuration, managed through a `.env` file. Here’s a brief explanation of each variable:

- **DATABASE_URL**: URL for connecting to the PostgreSQL database.
- **SECRET_KEY**: Secret key used for JWT token generation.
- **ALGORITHM**: The hashing algorithm for encoding JWT tokens (e.g., HS256).
- **ACCESS_TOKEN_EXPIRE_MINUTES**: Duration (in minutes) for which an access token is valid.
- **REFRESH_TOKEN_EXPIRE_DAYS**: Duration (in days) for which a refresh token is valid.

## Endpoints

### Auth
- **POST /api/v1/auth/login**: User login
- **POST /api/v1/auth/logout**: User logout
- **POST /api/v1/auth/refresh**: Refreshes aceess token
- **PUT /api/v1/auth/revoke/{user_id}**: Revokes user aceess token

### Users
- **POST /api/v1/users/register**: User registration
- **GET /api/v1/users/me**: Get current user
- **GET /api/v1/users**: Get all users
- **GET /api/v1/users/permissions/{category_id}**: Get users with permissions for given category
- **GET /api/v1/users/{user_id}/permissions**: Get permission to user
- **PUT /api/v1/users/{user_id}/permissions/{category_id}/read**: Grant read permission to user
- **PUT /api/v1/users/{user_id}/permissions/{category_id}/write**: Grant write permission to user
- **DELETE /api/v1/users/{user_id}/permissions/{category_id}/revoke**: Revoke permission from user

### Topics
- **GET /api/v1/topics/public**: Get public topics
- **GET /api/v1/topics**: Get all topics
- **GET /api/v1/topics/{topic_id}**: Get topic by ID
- **POST /api/v1/topics/{category_id}**: Create a new topic
- **PUT /api/v1/topics/{topic_id}**: Update a topic
- **PATCH /api/v1/topics/{topic_id}/lock**: Lock topic
- **PATCH /api/v1/topics/{topic_id}/replies/{reply_id}/best**: Select best reply for topic

### Replies
- **GET /api/v1/replies/{reply_id}**: Get reply by ID
- **POST /api/v1/replies/{topic_id}**: Create a new reply for a topic
- **PUT /api/v1/replies/{reply_id}**: Update a reply
- **PATCH /api/v1/replies/{reply_id}**: Upvote or downvote a reply

### Categories
- **POST /api/v1/categories**: Create a new category
- **GET /api/v1/categories**: Get all categories
- **GET /api/v1/categories/{category_id}/topics**: Get topics in a category
- **PUT /api/v1/categories/{category_id}/private**: Set category privacy
- **PUT /api/v1/categories/{category_id}/lock**: Lock or unlock a category

### Conversations
- **GET /api/v1/conversations/contacts**: Get users with conversations with currect user
- **GET /api/v1/conversations/{receiver_id}**: Get messages with a user

### Messages
- **POST /api/v1/messages**: Send a message
- **POST /api/v1/messages/by-username**: Send a message by username

### Websockets
- **GET /api/v1/ws/connect**: WebSocket connection

## Testing

To run the tests, use the following command:

```bash
python -m unittest discover -s tests -p "*_test.py"
```

This will run all tests in the `tests/` directory. Ensure that your `.env` file or test configuration uses a separate test database to avoid modifying production data.

## License

This project is licensed under the [MIT License](LICENSE).

---
