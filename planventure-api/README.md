# Planventure API 🌍✈️

A robust REST API built with Flask for managing travel plans and itineraries. The API provides authentication, trip management, and itinerary generation capabilities.

## Features

- 🔐 JWT-based authentication
- 📅 Trip planning and management
- 🗺️ Location tracking with coordinates
- 📋 Automatic itinerary generation
- 🔄 CORS support for frontend integration

## Tech Stack

- **Framework**: Flask 2.3.3
- **Database**: SQLite (via SQLAlchemy)
- **Authentication**: JWT (flask-jwt-extended)
- **Schema Validation**: Marshmallow
- **Security**: bcrypt for password hashing
- **Development**: Black, Flake8, Pytest

## Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)
- Git

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/planventure.git
cd planventure/planventure-api
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .sample.env .env
```

Update `.env` with your configurations:
```
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=your-database-url
CORS_ORIGIN=http://localhost:3000
CORS_METHODS=GET,POST,PUT,DELETE,OPTIONS
```

5. Initialize the database:
```bash
python create_db.py
```

## API Endpoints

### Authentication

- `POST /auth/register` - Register new user
- `POST /auth/login` - User login

### Trips

- `GET /trips` - List all trips
- `POST /trips` - Create new trip
- `GET /trips/<id>` - Get trip details
- `PUT /trips/<id>` - Update trip
- `DELETE /trips/<id>` - Delete trip

### System

- `GET /` - Welcome message
- `GET /health` - System health check

## Request Examples

### Register User
```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepass123"
  }'
```

### Create Trip
```bash
curl -X POST http://localhost:5000/trips \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -d '{
    "title": "Weekend in Paris",
    "description": "A romantic getaway",
    "location": "Paris, France",
    "start_date": "2024-06-15",
    "end_date": "2024-06-17",
    "latitude": 48.8566,
    "longitude": 2.3522
  }'
```

## Development

1. Start development server:
```bash
flask run --debug
```

2. Run tests:
```bash
pytest
```

3. Format code:
```bash
black .
```

4. Lint code:
```bash
flake8
```

## Project Structure

```
planventure-api/
├── app.py              # Application entry point
├── create_db.py        # Database initialization
├── database.py         # Database configuration
├── models/             # Database models
│   ├── user.py
│   └── trip.py
├── routes/             # API routes
│   ├── auth.py
│   └── trips.py
├── schemas/            # Data validation schemas
│   ├── auth.py
│   └── trip.py
├── utils/             # Utility functions
│   ├── jwt.py
│   ├── password.py
│   └── validation.py
└── tests/             # Test files
```

## Security

- Passwords are hashed using bcrypt
- JWT tokens for authentication
- CORS protection
- Input validation using marshmallow schemas
- Environment variable configuration

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.