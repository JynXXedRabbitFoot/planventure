from email_validator import validate_email, EmailNotValidError

def validate_email_format(email: str) -> tuple[bool, str]:
    """Validate email format and return (is_valid, error_message)."""
    try:
        validate_email(email)
        return True, ""
    except EmailNotValidError as e:
        return False, str(e)
