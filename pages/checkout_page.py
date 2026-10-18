import re
from playwright.sync_api import Page


class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page
        self.heading = page.get_by_text("Shipping & Delivery Address")
        self.full_name = page.get_by_label("Full Name")
        self.phone = page.get_by_label("Phone Number")
        self.email = page.get_by_label("Email Address")
        self.street = page.get_by_label("Street Address")
        self.city = page.get_by_label("City")
        self.state = page.get_by_label("State")
        self.pincode = page.get_by_label("Pincode")
        self.upi = page.get_by_role("radio", name=re.compile("UPI"))
        self.card = page.get_by_role("radio", name=re.compile("Debit Card"))
        self.cod = page.get_by_role("radio", name=re.compile("Cash on Delivery"))
        self.place_order = page.get_by_role("button", name="Place Order Now")

    def fill_address(self, street, city, state, pincode):
        self.street.fill(street)
        self.city.fill(city)
        self.state.fill(state)
        self.pincode.fill(pincode)