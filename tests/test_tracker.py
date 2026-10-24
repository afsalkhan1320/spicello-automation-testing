import re
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage

ADDRESS = {
    "street": "12 Gandhi Street, Anna Nagar",
    "city": "Chennai",
    "state": "Tamil Nadu",
    "pincode": "600001",
}


def open_track_page_from_menu(page: Page):
    LoginPage(page).open_user_menu()
    page.locator(".dropdown-menu").get_by_text("Track Order").click()


@pytest.fixture
def placed_order_number(checkout_page, base_url):
    """Place an order, go to the home page, return (page, order number)."""
    page = checkout_page.page
    checkout_page.cod.check()
    checkout_page.fill_address(**ADDRESS)
    checkout_page.place_order.click()
    expect(page.get_by_text("Order Placed Successfully!")).to_be_visible()
    match = re.search(r"#SPICE-(\d+)", page.locator("body").inner_text())
    assert match, "Order ID not found on the confirmation box"
    page.goto(base_url + "index.html", wait_until="domcontentloaded")
    return page, match.group(1)


@pytest.mark.regression
def test_user_menu_track_order_opens_search_page(page: Page, base_url, new_user):
    login = LoginPage(page)
    login.open(base_url)
    login.signup(**new_user)
    page.wait_for_timeout(1500)
    page.goto(base_url + "index.html", wait_until="domcontentloaded")

    open_track_page_from_menu(page)

    expect(page).to_have_url(re.compile(r"track\.html"))
    expect(page.get_by_role("heading", name="Track Your Spice Order")).to_be_visible()
    expect(page.get_by_text("Example ID: SPICE-84920")).to_be_visible()
    expect(page.get_by_role("textbox")).to_be_visible()
    expect(page.get_by_role("button", name="Track", exact=True)).to_be_visible()


@pytest.mark.regression
@pytest.mark.parametrize("prefix", ["", "#"], ids=["without_hash", "with_hash"])
def test_track_order_from_menu_finds_placed_order(placed_order_number, prefix):
    page, number = placed_order_number
    open_track_page_from_menu(page)
    page.get_by_role("textbox").fill(f"{prefix}SPICE-{number}")
    page.get_by_role("button", name="Track", exact=True).click()

    expect(page).to_have_url(re.compile(rf"track\.html\?id=SPICE-{number}"))
    body = page.locator("body")
    expect(body).to_contain_text("Order Status")
    expect(body).to_contain_text(re.compile(rf"Order ID:\s*#SPICE-{number}"))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
                                                          
    
    
    
    
    
    
    
    
    
    