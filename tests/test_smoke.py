import re
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.smoke
def test_home_page_loads(page: Page, base_url):
    page.goto(base_url,wait_until="domcontentloaded")
    expect(page).to_have_title(re.compile("Spicello"))
    expect(page.get_by_role("heading", name="ORGANIC SPICES")).to_be_visible()


@pytest.mark.smoke
def test_products_page_loads(page: Page, base_url):
    page.goto(base_url + "products.html")
    expect(page).to_have_url(re.compile("products.html"))
    expect(page.get_by_role("button", name="Add To Cart").first).to_be_visible()


@pytest.mark.smoke
def test_login_page_loads(page: Page, base_url):
    page.goto(base_url + "login.html")
    expect(page).to_have_url(re.compile("login.html"))
    expect(page.locator("input").first).to_be_visible()
    
@pytest.mark.smoke
def test_add_to_cart_updates_cart_count(page: Page, base_url):
    page.goto(base_url + "products.html")
    page.get_by_role("button", name="Add To Cart").first.click()
    expect(page.locator("nav")).to_contain_text("1")


@pytest.mark.smoke
def test_cart_panel_shows_added_product(page: Page, base_url):
    page.goto(base_url + "products.html")
    page.get_by_role("button", name="Add To Cart").first.click()
    page.locator("[data-bs-toggle='offcanvas']").first.click()
    expect(page.get_by_text("Your Shopping Cart")).to_be_visible()
    expect(page.get_by_text(re.compile(r"100gm.*Rs\. 29\.00"))).to_be_visible()