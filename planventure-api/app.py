from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from database import db
from flask_jwt_extended import JWTManager
from routes.auth import auth_bp
from routes.trips import trips_bp

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure CORS
CORS(app, resources={
    r"/*": {
        "origins": os.getenv('CORS_ORIGIN', 'http://localhost:3000'),
        "methods": os.getenv('CORS_METHODS', 'GET,POST,PUT,DELETE,OPTIONS').split(','),
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Range", "X-Content-Range"],
        "supports_credentials": True,
        "max_age": 600
    }
})

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///planventure.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-please-change')

# Initialize extensions
db.init_app(app)

# JWT Configuration
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-key-please-change')
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=4)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_HEADER_NAME"] = "Authorization"
app.config["JWT_HEADER_TYPE"] = "Bearer"
app.config["JWT_JSON_KEY"] = "access_token"
app.config["JWT_ENCODE_ISSUER"] = "planventure-api"
app.config["JWT_DECODE_ISSUER"] = "planventure-api"
app.config["JWT_ENCODE_AUDIENCE"] = "planventure-client"
app.config["JWT_DECODE_AUDIENCE"] = "planventure-client"
app.config["JWT_IDENTITY_CLAIM"] = "sub"
app.config["JWT_ERROR_MESSAGE_KEY"] = "error"

# Initialize JWT
jwt = JWTManager(app)

# Enhanced JWT error handlers
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"error": "Token has expired"}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"error": f"Invalid token: {error}"}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({"error": "Authorization token is missing"}), 401

@jwt.token_verification_failed_loader
def verification_failed_callback(jwt_header, jwt_payload):
    return jsonify({"error": "Token verification failed"}), 401

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    return False  # Implement token blocklist if needed

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(trips_bp, url_prefix='/trips')

# Import models after db initialization to avoid circular imports
from models.user import User
from models.trip import Trip

@app.route('/')
def home():
    return jsonify({"message": "Welcome to PlanVenture API"})

@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    })

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
