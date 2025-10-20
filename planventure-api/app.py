from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from database import db
from flask_jwt_extended import JWTManager
from routes.auth import auth_bp

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///planventure.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-please-change')

# Initialize extensions
db.init_app(app)
CORS(app)

# Initialize JWT
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-me')
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

# Initialize JWT error handlers
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"error": "Token has expired"}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"error": "Invalid token"}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({"error": "Authorization token is missing"}), 401

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')

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
        db.create_all()  # Create database tables
    app.run(debug=True)
