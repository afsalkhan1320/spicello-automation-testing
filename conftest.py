import pytest
import time


BASE_URL = "https://spicello.vercel.app/"

@pytest.fixture(scope="session")
def base_url():
    return BASE_URL

 

@pytest.fixture
def new_user():
    stamp = int(time.time())
    return {
        "name": "UserTest1",
        "phone": f"9{stamp % 10**9:09d}",
        "email": f"test{stamp}@example.com",
        "password": "Test@1234",
    }