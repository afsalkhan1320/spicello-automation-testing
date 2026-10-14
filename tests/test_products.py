import re
import pytest
from playwright.sync_api import Page, expect

PRODUCTS = [
    ("p1", "Turmeric Powder", "Rs. 29.00"),
    ("p2", "Chilli Powder", "Rs. 40.00"),
    ("p3", "Coriander Powder", "Rs. 24.00"),
    ("p4", "Cumin Powder", "Rs. 90.00"),
    ("p5", "Pepper Powder", "Rs. 88.00"),
    ("p6", "Fennel Powder", "Rs. 40.00"),
    ("p7", "Garam Masala", "Rs. 75.00"),
    ("p8", "Cardamom Powder", "Rs. 150.00"),
    ("p9", "Ginger Powder", "Rs. 65.00"),
]


@pytest.mark.smoke
def test_all_nine_products_are_listed(page: Page, base_url):
    page.goto(base_url + "products.html", wait_until="domcontentloaded")
    expect(page.get_by_role("button", name="Add To Cart")).to_have_count(9)


@pytest.mark.regression
@pytest.mark.parametrize("product_id, name, price", PRODUCTS)
def test_product_opens_correct_detail_page(page: Page, base_url, product_id, name, price):
    page.goto(base_url + "products.html", wait_until="domcontentloaded")
    page.get_by_role("link", name=name, exact=True).first.click()
    expect(page).to_have_url(re.compile(rf"product-detail\.html\?id={product_id}"))
    expect(page.get_by_role("heading", name=name, level=1)).to_be_visible()
    expect(page.get_by_role("heading", name=price, level=3)).to_be_visible()


@pytest.mark.regression
def test_quantity_buttons_change_quantity(page: Page, base_url):
    page.goto(base_url + "product-detail.html?id=p1", wait_until="domcontentloaded")
    qty = page.get_by_role("textbox", name="Quantity")
    expect(qty).to_have_value("1")
    page.get_by_role("button", name="Increase quantity").click()
    expect(qty).to_have_value("2")
    page.get_by_role("button", name="Decrease quantity").click()
    expect(qty).to_have_value("1")


@pytest.mark.regression
def test_back_to_spices_link(page: Page, base_url):
    page.goto(base_url + "product-detail.html?id=p1", wait_until="domcontentloaded")
    page.get_by_role("link", name="Back to Spices").click()
    expect(page).to_have_url(re.compile("products.html"))


@pytest.mark.regression
def test_add_to_cart_from_detail_page(page: Page, base_url):
    page.goto(base_url + "product-detail.html?id=p1", wait_until="domcontentloaded")
    page.get_by_role("button", name="Add to Cart").first.click()
    expect(page.locator("nav.navbar")).to_contain_text("1")