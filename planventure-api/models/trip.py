from database import db, TimestampMixin
from datetime import datetime
from utils.itinerary import generate_itinerary_template
from sqlalchemy import event

class Trip(TimestampMixin, db.Model):
    __tablename__ = 'trips'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    location = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    itinerary = db.Column(db.JSON)
    
    # Relationship
    user = db.relationship('User', back_populates='trips')

    def __repr__(self):
        return f'<Trip {self.title} ({self.start_date} - {self.end_date})>'

    def generate_default_itinerary(self):
        """Generate a default itinerary based on trip dates."""
        return generate_itinerary_template(self.start_date, self.end_date)

    def to_dict(self):
        """Convert trip to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'itinerary': self.itinerary,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

@event.listens_for(Trip, 'before_insert')
def set_default_itinerary(mapper, connection, target):
    """Generate default itinerary before insert if none exists"""
    if target.itinerary is None:
        target.itinerary = target.generate_default_itinerary()
