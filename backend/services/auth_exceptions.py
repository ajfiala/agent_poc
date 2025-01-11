from functools import wraps
from fastapi import HTTPException, status

class InvalidTokenException(Exception):
    """Custom exception for invalid token or token-based checks."""

def handle_invalid_token(func):
    """
    Decorator to catch InvalidTokenException and raise a 401 HTTPException.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except InvalidTokenException as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e) or "Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            ) from e
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e) or "Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            ) from e
    return wrapper
