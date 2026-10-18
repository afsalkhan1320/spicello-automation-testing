import re
import pytest
from playwright.sync_api import expect

ADDRESS = {
    "street": "12 Gandhi Street, Anna Nagar",
    "city": "Chennai",
    "state": "Tamil Nadu",
    "pincode": "600001",
}


@pytest.fixture
def tracked_order(checkout_page):
    """Place an order, remember its number, then click Track Your Order."""
    page = checkout_page.page
    checkout_page.cod.check()
    checkout_page.fill_address(**ADDRESS)
    checkout_page.place_order.click()
    expect(page.get_by_text("Order Placed Successfully!")).to_be_visible()

    match = re.search(r"#SPICE-(\d+)", page.locator("body").inner_text())
    assert match, "Order ID not found on the confirmation box"
    order_number = match.group(1)

    page.get_by_text("Track Your Order").click()
    return page, order_number


@pytest.mark.checkout
def test_track_your_order_opens_order_status_page(tracked_order):
    page, number = tracked_order
    expect(page).to_have_url(re.compile(rf"track\.html\?id=SPICE-{number}"))
    expect(page.get_by_role("heading", name="Order Status")).to_be_visible()
    body = page.locator("body")
    expect(body).to_contain_text(re.compile(rf"Order ID:\s*#SPICE-{number}"))
    expect(body).to_contain_text(re.compile(r"Placed on:\s*\w+ \d{1,2}, \d{4}"))


@pytest.mark.checkout
def test_order_status_shows_shipping_address(tracked_order, new_user):
    page, _ = tracked_order
    body = page.locator("body")
    expect(body).to_contain_text("Shipping Address")
    expect(body).to_contain_text(new_user["name"])
    expect(body).to_contain_text(ADDRESS["street"])
    expect(body).to_contain_text(ADDRESS["city"])
    expect(body).to_contain_text(ADDRESS["pincode"])
    expect(body).to_contain_text(new_user["phone"])


@pytest.mark.checkout
def test_order_status_shows_items_and_totals(tracked_order):
    page, _ = tracked_order
    body = page.locator("body")
    expect(body).to_contain_text("Items Ordered")
    expect(body).to_contain_text(re.compile(r"Turmeric Powder\s*Quantity: 1"))
    expect(body).to_contain_text(re.compile(r"Chilli Powder\s*Quantity: 1"))
    expect(body).to_contain_text(re.compile(r"Subtotal\s*Rs\.\s*69\.00"))
    expect(body).to_contain_text(re.compile(r"Shipping Fee\s*Rs\.\s*30\.00"))
    expect(body).to_contain_text(re.compile(r"Total Paid\s*Rs\.\s*99\.00"))


@pytest.mark.checkout
def test_order_status_shows_progress_steps(tracked_order):
    page, _ = tracked_order
    body = page.locator("body")
    for step in ["Order Placed", "Packed", "In Transit", "Delivered"]:
        expect(body).to_contain_text(step)
    expect(body).to_contain_text("Estimated Delivery")
    expect(body).to_contain_text("2-3 business days")
@pytest.fixture
def placed_order(checkout_page):
    page = checkout_page.page
    checkout_page.cod.check()
    checkout_page.fill_address(**ADDRESS)
    checkout_page.place_order.click()
    expect(page.get_by_text("Order Placed Successfully!")).to_be_visible()
    return page


@pytest.mark.checkout
def test_back_to_home_page_goes_to_home(placed_order):
    page = placed_order
    page.get_by_text("Back to Home Page").click()
    expect(page).to_have_url(re.compile(r"index\.html|/$"))
    expect(page.get_by_role("heading", name="ORGANIC SPICES")).to_be_visible()


@pytest.mark.checkout
def test_cart_is_empty_after_order(placed_order, base_url):
    page = placed_order
    page.goto(base_url + "cart.html", wait_until="domcontentloaded")
    expect(page.get_by_text("Your Shopping Cart is Empty")).to_be_visible()