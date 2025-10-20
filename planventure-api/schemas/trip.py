from marshmallow import Schema, fields, validate, ValidationError
from datetime import datetime

class TripSchema(Schema):
    """Schema for Trip model serialization/deserialization"""
    
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str(validate=validate.Length(max=500))
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    location = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    latitude = fields.Float(allow_none=True)
    longitude = fields.Float(allow_none=True)
    itinerary = fields.Dict(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    user_id = fields.Int(dump_only=True)

    # Add validation
    def validate_dates(self, data):
        if data['end_date'] < data['start_date']:
            raise ValidationError('End date must be after start date')
        return data

# Usage in routes:
"""
@trips_bp.route('/', methods=['POST'])
def create_trip():
    try:
        schema = TripSchema()
        trip_data = schema.load(request.json)  # Use load() instead of .data
        
        trip = Trip(**trip_data)
        db.session.add(trip)
        db.session.commit()
        
        return jsonify(schema.dump(trip)), 201  # Use dump() instead of .data
        
    except ValidationError as err:
        return jsonify({"error": "Validation failed", "messages": err.messages}), 400
"""
