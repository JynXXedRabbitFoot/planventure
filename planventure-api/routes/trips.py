from flask import Blueprint, request, jsonify
from models.trip import Trip
from database import db
from schemas.trip import TripSchema
from middleware.auth import auth_required, get_current_user
from marshmallow import ValidationError

trips_bp = Blueprint('trips', __name__)

@trips_bp.route('/', methods=['POST'])
@auth_required()
def create_trip():
    schema = TripSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({"error": "Validation failed", "messages": err.messages}), 400

    current_user = get_current_user()
    trip = Trip(user_id=current_user.id, **data)
    
    db.session.add(trip)
    db.session.commit()
    
    return jsonify(schema.dump(trip)), 201

@trips_bp.route('/', methods=['GET'])
@auth_required()
def get_trips():
    current_user = get_current_user()
    trips = current_user.trips.all()
    return jsonify(TripSchema(many=True).dump(trips))

@trips_bp.route('/<int:trip_id>', methods=['GET'])
@auth_required()
def get_trip(trip_id):
    current_user = get_current_user()
    trip = current_user.trips.filter_by(id=trip_id).first_or_404()
    return jsonify(TripSchema().dump(trip))

@trips_bp.route('/<int:trip_id>', methods=['PUT'])
@auth_required()
def update_trip(trip_id):
    schema = TripSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({"error": "Validation failed", "messages": err.messages}), 400

    current_user = get_current_user()
    trip = current_user.trips.filter_by(id=trip_id).first_or_404()
    
    for key, value in data.items():
        setattr(trip, key, value)
    
    db.session.commit()
    return jsonify(schema.dump(trip))

@trips_bp.route('/<int:trip_id>', methods=['DELETE'])
@auth_required()
def delete_trip(trip_id):
    current_user = get_current_user()
    trip = current_user.trips.filter_by(id=trip_id).first_or_404()
    
    db.session.delete(trip)
    db.session.commit()
    
    return '', 204
