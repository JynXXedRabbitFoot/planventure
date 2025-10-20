from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from datetime import datetime
import logging

def generate_tokens(user_id: int) -> dict:
    """
    Generate access and refresh tokens for a user.
    
    Args:
        user_id (int): The user's ID
        
    Returns:
        dict: Dictionary containing access and refresh tokens
    """
    try:
        # Convert user_id to string and add claims
        user_id_str = str(user_id)
        additional_claims = {
            "type": "access",
            "user_id": user_id_str
        }
        
        # Generate tokens
        access_token = create_access_token(
            identity=user_id_str,
            additional_claims=additional_claims
        )
        
        refresh_token = create_refresh_token(
            identity=user_id_str
        )

        # Verify token structure
        try:
            decoded = decode_token(access_token)
            if not decoded:
                raise ValueError("Token validation failed")
        except Exception as e:
            raise ValueError(f"Token generation error: {str(e)}")

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer'
        }
        
    except Exception as e:
        logging.error(f"Token generation failed: {str(e)}")
        raise ValueError(f"Token generation error: {str(e)}")
