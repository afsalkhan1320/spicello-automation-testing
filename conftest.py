import time
import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.checkout_page import CheckoutPage

BASE_URL = "https://spicello.vercel.app/"


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture
def new_user():
    stamp = int(time.time())
    return {
        "name": "Rajkumar",
        "phone": f"9{stamp % 10**9:09d}",
        "email": f"test{stamp}@example.com",
        "password": "Test@1234",
    }


@pytest.fixture
def checkout_page(page, base_url, new_user):
    login = LoginPage(page)
    login.open(base_url)
    login.signup(**new_user)
    page.wait_for_timeout(1500)

    page.goto(base_url + "products.html", wait_until="domcontentloaded")
    buttons = page.get_by_role("button", name="Add To Cart")
    buttons.nth(0).click()
    buttons.nth(1).click()
    page.goto(base_url + "cart.html", wait_until="domcontentloaded")
    page.get_by_role("button", name="Proceed to Checkout").click()

    checkout = CheckoutPage(page)
    expect(checkout.heading).to_be_visible()
    return checkout



    