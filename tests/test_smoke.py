import re
import pytest
from playwright.sync_api import Page, expect

@pytest.mark.smoke
def test_home_page_loads(page: Page, base_url):
    page.goto(base_url)
    expect(page).to_have_title(re.compile("Spicello"))
    expect(page.get_by_role("heading", name="ORGANIC SPICES")).to_be_visible()

@pytest.mark.smoke
def test_products_page_loads(page: Page, base_url):
    page.goto(base_url + "products.html")
    expect(page).to_have_url(re.compile("products.html"))
    expect(page.get_by_role("button", name="Add To Cart").first).to_be_visible()


def test_login_page_loads(page: Page, base_url):
    page.goto(base_url + "login.html")
    expect(page).to_have_url(re.compile("login.html"))
    expect(page.locator("input").first).to_be_visible()