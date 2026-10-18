import re
import pytest
from playwright.sync_api import expect

VALID_ADDRESS = {
    "street": "12 Gandhi Street, Anna Nagar",
    "city": "Chennai",
    "state": "Tamil Nadu",
    "pincode": "600001",
}


# ---------- Prefilled data ----------
@pytest.mark.checkout
def test_name_phone_email_are_prefilled_from_account(checkout_page, new_user):
    expect(checkout_page.full_name).to_have_value(new_user["name"])
    expect(checkout_page.phone).to_have_value(new_user["phone"])
    expect(checkout_page.email).to_have_value(new_user["email"])


# ---------- Payment method ----------
@pytest.mark.checkout
def test_upi_is_selected_by_default(checkout_page):
    expect(checkout_page.upi).to_be_checked()
    expect(checkout_page.card).not_to_be_checked()
    expect(checkout_page.cod).not_to_be_checked()


@pytest.mark.checkout
def test_selecting_cod_selects_only_cod(checkout_page):
    checkout_page.cod.check()
    expect(checkout_page.cod).to_be_checked()
    expect(checkout_page.upi).not_to_be_checked()
    expect(checkout_page.card).not_to_be_checked()


@pytest.mark.checkout
def test_switching_payment_method_deselects_previous(checkout_page):
    checkout_page.cod.check()
    checkout_page.upi.check()
    expect(checkout_page.upi).to_be_checked()
    expect(checkout_page.cod).not_to_be_checked()


# ---------- Order summary ----------
@pytest.mark.checkout
def test_checkout_summary_matches_cart(checkout_page):
    page = checkout_page.page
    expect(page.get_by_role("heading", name="Turmeric Powder", level=6)).to_be_visible()
    expect(page.get_by_role("heading", name="Chilli Powder", level=6)).to_be_visible()
    body = page.locator("body")
    expect(body).to_contain_text(re.compile(r"Subtotal\s*Rs\.\s*69\.00"))
    expect(body).to_contain_text(re.compile(r"Shipping Charge\s*Rs\.\s*30\.00"))
    expect(body).to_contain_text(re.compile(r"Total Amount\s*Rs\.\s*99\.00"))


# ---------- Placing the order ----------
@pytest.mark.checkout
def test_place_order_with_valid_details(checkout_page, new_user):
    page = checkout_page.page
    checkout_page.cod.check()
    checkout_page.fill_address(**VALID_ADDRESS)
    checkout_page.place_order.click()
    expect(page.get_by_text("Order Placed Successfully!")).to_be_visible()
    body = page.locator("body")
    expect(body).to_contain_text(re.compile(r"Order ID:\s*#SPICE-\d+"))
    expect(body).to_contain_text(re.compile(r"Deliver To:\s*" + re.escape(new_user["name"])))
    expect(page.get_by_text("Track Your Order")).to_be_visible()
    expect(page.get_by_text("Back to Home Page")).to_be_visible()


# ---------- Blocked orders ----------
@pytest.mark.checkout
def test_place_order_with_all_address_fields_empty(checkout_page):
    page = checkout_page.page
    checkout_page.cod.check()
    checkout_page.place_order.click()
    page.wait_for_timeout(1000)
    message = page.evaluate("document.getElementById('chk-address').validationMessage")
    assert message != "", "Street Address should be flagged invalid when empty"
    expect(page.get_by_text("Order Placed Successfully!")).not_to_be_visible()


@pytest.mark.checkout
@pytest.mark.parametrize("missing, field_id", [
    ("street", "chk-address"),
    ("city", "chk-city"),
    ("state", "chk-state"),
    ("pincode", "chk-pincode"),
])
def test_order_blocked_when_one_field_is_missing(checkout_page, missing, field_id):
    page = checkout_page.page
    checkout_page.cod.check()
    data = dict(VALID_ADDRESS)
    data[missing] = ""
    checkout_page.fill_address(**data)
    checkout_page.place_order.click()
    page.wait_for_timeout(1000)
    message = page.evaluate(f"document.getElementById('{field_id}').validationMessage")
    assert message != "", f"{field_id} should be flagged invalid"
    expect(page.get_by_text("Order Placed Successfully!")).not_to_be_visible()