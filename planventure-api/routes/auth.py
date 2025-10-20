from flask import Blueprint, request, jsonify
from models.user import User
from database import db
from schemas.auth import RegistrationSchema, LoginSchema
from utils.validation import validate_email_format
from marshmallow import ValidationError
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    schema = RegistrationSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({"error": "Validation failed", "messages": err.messages}), 400

    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 409

    # Create new user
    user = User(email=data['email'])
    user.password = data['password']  # This will hash the password

    db.session.add(user)
    db.session.commit()

    # Generate tokens
    tokens = user.generate_auth_tokens()
    
    return jsonify({
        "message": "User registered successfully",
        "tokens": tokens
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    schema = LoginSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({"error": "Validation failed", "messages": err.messages}), 400

    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.verify_password(data['password']):
        return jsonify({"error": "Invalid email or password"}), 401
    
    if not user.is_active:
        return jsonify({"error": "Account is deactivated"}), 403

    # Update last login
    user.last_login = datetime.utcnow()
    db.session.commit()

    # Generate tokens
    tokens = user.generate_auth_tokens()
    
    return jsonify({
        "message": "Login successful",
        "tokens": tokens,
        "user": {
            "id": user.id,
            "email": user.email
        }
    })
