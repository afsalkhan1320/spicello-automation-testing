import pytest

BASE_URL = "https://spicello.vercel.app/"

@pytest.fixture(scope="session")
def base_url():
    return BASE_URL