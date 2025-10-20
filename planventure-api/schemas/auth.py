from marshmallow import Schema, fields, validates, ValidationError
from utils.validation import validate_email_format

class RegistrationSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    
    @validates('password')
    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError('Password must be at least 8 characters long')

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
