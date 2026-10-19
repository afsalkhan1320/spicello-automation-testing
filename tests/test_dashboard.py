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


@pytest.fixture
def dashboard(page: Page, base_url, new_user):
    """A new, logged-in user on the dashboard (no orders yet)."""
    login = LoginPage(page)
    login.open(base_url)
    login.signup(**new_user)
    page.wait_for_timeout(1500)
    page.goto(base_url + "user.html", wait_until="domcontentloaded")
    return page


@pytest.fixture
def dashboard_with_order(checkout_page, base_url):
    """A logged-in user who has placed one order, standing on the dashboard."""
    page = checkout_page.page
    checkout_page.cod.check()
    checkout_page.fill_address(**ADDRESS)
    checkout_page.place_order.click()
    expect(page.get_by_text("Order Placed Successfully!")).to_be_visible()
    number = re.search(r"#SPICE-(\d+)", page.locator("body").inner_text()).group(1)
    page.goto(base_url + "user.html", wait_until="domcontentloaded")
    return page, number


@pytest.mark.regression
def test_dashboard_opens_from_user_menu(page: Page, base_url, new_user):
    login = LoginPage(page)
    login.open(base_url)
    login.signup(**new_user)
    page.wait_for_timeout(1500)
    login.open_user_menu()
    page.get_by_text("My Dashboard").click()
    expect(page).to_have_url(re.compile(r"user\.html"))
    expect(page).to_have_title(re.compile("My Account"))


@pytest.mark.regression
def test_dashboard_shows_account_name_and_email(dashboard, new_user):
    body = dashboard.locator("body")
    expect(body).to_contain_text(new_user["name"])
    expect(body).to_contain_text(new_user["email"])


@pytest.mark.regression
def test_profile_details_are_prefilled(dashboard, new_user):
    dashboard.get_by_text("Profile Details").first.click()
    expect(dashboard.get_by_label("Full Name")).to_have_value(new_user["name"])
    expect(dashboard.get_by_label("Phone Number")).to_have_value(new_user["phone"])
    email = dashboard.get_by_label("Email Address")
    expect(email).to_have_value(new_user["email"])
    expect(email).not_to_be_editable()


@pytest.mark.regression
def test_placed_order_appears_in_my_orders(dashboard_with_order):
    page, number = dashboard_with_order
    page.get_by_text("My Orders").first.click()
    body = page.locator("body")
    expect(body).to_contain_text(re.compile(rf"Order ID:\s*#SPICE-{number}"))
    expect(body).to_contain_text(re.compile(r"Turmeric Powder\s*100gm\s*•\s*Qty:\s*1"))
    expect(body).to_contain_text(re.compile(r"Chilli Powder\s*100gm\s*•\s*Qty:\s*1"))
    expect(body).to_contain_text(re.compile(r"Total Paid:\s*Rs\.\s*99\.00"))
    expect(body).to_contain_text("Packed")


@pytest.mark.regression
def test_track_order_button_opens_tracking_page(dashboard_with_order):
    page, number = dashboard_with_order
    page.get_by_text("My Orders").first.click()
    page.locator("a:visible, button:visible", has_text="Track Order").click()
    expect(page).to_have_url(re.compile(rf"track\.html\?id=SPICE-{number}"))