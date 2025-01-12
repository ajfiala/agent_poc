from fastapi import Depends, HTTPException, status, Request
from fastapi.security import APIKeyCookie
from typing import Optional
import jwt
import os
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.session import get_db_session
from dotenv import load_dotenv
from backend.db.repositories.guest import GuestRepository
from .auth_exceptions import InvalidTokenException, handle_invalid_token

load_dotenv()  

cookie_security = APIKeyCookie(name="access-token", auto_error=False)
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def create_access_token(guest_id: int, email: str) -> str:
    """
    Create a JWT access token for the guest.
    """

    print(f"secret key: {SECRET_KEY}  algorithm: {ALGORITHM}")

    payload = {
        "guest_id": guest_id,
        "email": email,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)



    print(f"Created token for guest_id {guest_id} with email {email}")

    print(f"Token: {token}")

    return token

async def get_token_from_cookie(token_from_cookie: Optional[str] = Depends(cookie_security)):
    if not token_from_cookie:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing access token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_from_cookie

@handle_invalid_token
async def validate_guest(
    request: Request,
    async_session: AsyncSession = Depends(get_db_session),
    token: Optional[str] = Depends(get_token_from_cookie)
):
    """
    Validate the guest based on the provided token.
    Raises InvalidTokenException if anything fails.
    """
    if not token:
        raise InvalidTokenException("Missing token in cookie")  
    # decode token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    except jwt.PyJWTError:
        raise InvalidTokenException("Token decode error")

    guest_id = payload.get("guest_id")
    email = payload.get("email")
    if not guest_id or not email:
        raise InvalidTokenException("Invalid token: missing guest_id/email")

    guest_repo = GuestRepository(db=async_session)
    guest = await guest_repo.get_guest_by_id(guest_id=guest_id)
    
    if guest.email != email:
        raise InvalidTokenException("Token email does not match guest")
    
    return guest
