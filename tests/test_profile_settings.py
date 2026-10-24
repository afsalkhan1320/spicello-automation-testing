import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.checkout_page import CheckoutPage

PROFILE = {
    "name": "Meenakshi",
    "street": "Azad Nagar, 1st Street",
    "city": "Chennai",
    "pincode": "600029",
}


def new_phone(new_user):
    # same length as the signup phone, but a different number
    return "8" + new_user["phone"][1:]


def sign_up_and_save_profile(page: Page, base_url, new_user):
    login = LoginPage(page)
    login.open(base_url)
    login.signup(**new_user)
    page.wait_for_timeout(1500)

    page.goto(base_url + "user.html", wait_until="domcontentloaded")
    page.get_by_text("Profile Details").first.click()
    page.get_by_label("Full Name").fill(PROFILE["name"])
    page.get_by_label("Phone Number").fill(new_phone(new_user))
    page.get_by_placeholder("Door No., Street name").fill(PROFILE["street"])
    page.get_by_label("City").fill(PROFILE["city"])
    page.get_by_label("Pincode").fill(PROFILE["pincode"])
    page.get_by_text("Save Profile Settings").click()
    page.wait_for_timeout(1500)


@pytest.mark.regression
def test_saved_profile_is_prefilled_on_checkout(page: Page, base_url, new_user):
    sign_up_and_save_profile(page, base_url, new_user)

    page.goto(base_url + "products.html", wait_until="domcontentloaded")
    buttons = page.get_by_role("button", name="Add To Cart")
    buttons.nth(0).click()
    buttons.nth(1).click()
    page.goto(base_url + "cart.html", wait_until="domcontentloaded")
    page.get_by_role("button", name="Proceed to Checkout").click()

    checkout = CheckoutPage(page)
    expect(checkout.heading).to_be_visible()
    expect(checkout.full_name).to_have_value(PROFILE["name"])
    expect(checkout.phone).to_have_value(new_phone(new_user))
    expect(checkout.email).to_have_value(new_user["email"])
    expect(checkout.street).to_have_value(PROFILE["street"])
    expect(checkout.city).to_have_value(PROFILE["city"])
    expect(checkout.pincode).to_have_value(PROFILE["pincode"])


@pytest.mark.regression
def test_saved_profile_persists_after_reload(page: Page, base_url, new_user):
    sign_up_and_save_profile(page, base_url, new_user)

    page.reload(wait_until="domcontentloaded")
    page.get_by_text("Profile Details").first.click()
    expect(page.get_by_label("Full Name")).to_have_value(PROFILE["name"])
    expect(page.get_by_label("Phone Number")).to_have_value(new_phone(new_user))
    expect(page.get_by_placeholder("Door No., Street name")).to_have_value(PROFILE["street"])
    expect(page.get_by_label("City")).to_have_value(PROFILE["city"])
    expect(page.get_by_label("Pincode")).to_have_value(PROFILE["pincode"])