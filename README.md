# Polls API

A Flask-based REST API for voting in polls with different access levels. This API is designed to teach web security best practices through incremental improvements.

## Features

- **Public Polls**: Anyone can vote without authentication
- **Protected Polls**: Requires user authentication to vote
- **Admin Polls**: Requires admin role to vote

## Tech Stack

- Flask 3.0.0
- Flask-SQLAlchemy (SQLite database)
- Flask-CORS
- Flask-JWT-Extended (JWT authentication)

## Setup

1. Create and activate a virtual environment:

   **Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   **Linux/Mac:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register a new user
  ```json
  {
    "username": "user123",
    "password": "password123"
  }
  ```

- `POST /api/auth/login` - Login and get JWT token
  ```json
  {
    "username": "user123",
    "password": "password123"
  }
  ```

### Polls

- `GET /api/polls` - Get all polls
- `GET /api/polls/<id>` - Get a specific poll
- `POST /api/polls` - Create a new poll (requires authentication)
  ```json
  {
    "question": "What is your favorite color?",
    "is_public": true,
    "requires_admin": false
  }
  ```

### Votes

- `POST /api/votes/poll/<poll_id>` - Vote on a poll
  ```json
  {
    "choice": "Blue"
  }
  ```

- `GET /api/votes/poll/<poll_id>` - Get all votes for a poll

## Authentication

For protected endpoints, include the JWT token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## Security Notes

This is a basic implementation designed for educational purposes. The following security considerations are intentionally simplified and can be improved in subsequent lessons:

- Password storage (currently using werkzeug, but can be improved)
- JWT token handling
- Input validation
- SQL injection prevention (SQLAlchemy helps, but can be improved)
- Rate limiting
- CORS configuration
- Error handling and information disclosure

## Database

The application uses SQLite by default. The database file (`polls.db`) will be created automatically on first run.

**Note**: The first user registered automatically becomes an admin for demo purposes.

