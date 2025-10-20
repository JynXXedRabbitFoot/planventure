from database import db, TimestampMixin
from datetime import datetime
from utils.password import hash_password, verify_password
from utils.jwt import generate_tokens

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

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = hash_password(password)

    def verify_password(self, password):
        return verify_password(password, self.password_hash)

    def generate_auth_tokens(self) -> dict:
        """Generate authentication tokens for the user."""
        return generate_tokens(self.id)

    def to_dict(self):
        """Return a dictionary representation of the user."""
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            "last_login": self.last_login.isoformat() if self.last_login else None
        }
