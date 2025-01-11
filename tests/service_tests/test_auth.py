import pytest
import pytest_asyncio
from fastapi import FastAPI, Depends
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from starlette.status import HTTP_401_UNAUTHORIZED
import time 
from backend.db.session import get_db_session
from backend.services.auth import get_token_from_cookie, validate_guest, create_access_token

app = FastAPI()

@app.get("/protected")
async def protected_route(
    token: str = Depends(get_token_from_cookie),
    guest=Depends(validate_guest)
):
    return {"success": True, "guest": guest}

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac

@pytest.mark.asyncio
async def test_cookie_missing_fails(client: AsyncClient):
    response = await client.get("/protected")
    assert response.status_code == HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Missing access token"}

@pytest.mark.asyncio
async def test_cookie_present(client: AsyncClient):
    token_value = create_access_token(3, "chris.cheeseburger@oddmail.net")
    client.cookies.set("access-token", token_value)
    response = await client.get("/protected")
    print(f"Response: {response.text}")

    assert response.status_code == 200
