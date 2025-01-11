import pytest
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from starlette.status import HTTP_401_UNAUTHORIZED
from backend.services.auth import get_token_from_cookie, validate_guest

app = FastAPI()

# Example protected endpoint that uses both dependencies
@app.get("/protected")
async def protected_route(
    token: str = Depends(get_token_from_cookie),
    guest=Depends(validate_guest),
):
    """
    If the user passes a valid cookie, and validate_guest
    confirms a real guest, we return a success response.
    Otherwise, we return 401.
    """
    return {"success": True, "guest": guest}


@pytest.fixture
def client():
    """
    Synchronous test fixture for using TestClient
    with our mini FastAPI test app.
    """
    return TestClient(app)

def test_cookie_missing_fails(client):
    """
    Ensure that if we don't provide the 'access-token' cookie,
    we get a 401 from get_token_from_cookie.
    """
    response = client.get("/protected")
    assert response.status_code == HTTP_401_UNAUTHORIZED
    assert response.json() == {
        "detail": "Missing access token"
    }

def test_cookie_present_but_not_implemented_yet(client):
    """
    If there's a cookie, we next depend on validate_guest,
    which is not implemented yet -> should raise NotImplementedError
    or eventually 401 if invalid token.
    """
    cookies = {"access-token": "some_fake_token"}
    # Expect 500 or NotImplemented, i.e. a fail, until we implement
    response = client.get("/protected", cookies=cookies)
    assert response.status_code == 200  # or 501, or something that fails