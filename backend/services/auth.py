from fastapi import Depends, HTTPException, status, Request
from fastapi.security import APIKeyCookie
from typing import Optional
from backend.db.repositories.guest import GuestRepository

cookie_security = APIKeyCookie(name="access-token", auto_error=False)

async def get_token_from_cookie(token_from_cookie: Optional[str] = Depends(cookie_security)):
    if not token_from_cookie:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing access token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_from_cookie

async def validate_guest(request: Request, token: Optional[str] = Depends(get_token_from_cookie)):
    """
    Validate the guest based on the provided token.
    This function is a placeholder and should be implemented
    to check the validity of the token and retrieve guest information.
    """
    raise NotImplementedError("Guest validation not implemented yet.")