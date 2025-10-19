from database import db, TimestampMixin
from datetime import datetime

class User(TimestampMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    last_login = db.Column(db.DateTime, default=None)

    # Relationships
    trips = db.relationship('Trip', back_populates='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.email}>'
