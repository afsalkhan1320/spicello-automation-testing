import re 
import pytest
from playwright.sync_api import Page,expect

def add_two_products(page:Page,base_url):
    page.goto(base_url + "products.html",wait_until="domcontentloaded")
    buttons=page.get_by_role("button", name="Add To Cart")
    buttons.nth(0).click()
    buttons.nth(1).click()
    
def open_cart(page:Page):
    page.locator("[data-bs-toggle=offcanvas]").first.click()   

@pytest.mark.regression 
def test_open_cartPage(page:Page,base_url):
    add_two_products(page, base_url)
    open_cart(page)
    page.get_by_text("View Full Cart Page").click()
    expect(page).to_have_url(re.compile("cart.html"))
    
@pytest.mark.regression
def test_shopping_cart_lists_both_products(page:Page,base_url):
    add_two_products(page, base_url)
    open_cart(page)
    page.get_by_text("View Full Cart Page").click()
    expect(page.get_by_role("heading", name="Turmeric Powder", level=5)).to_be_visible()
    expect(page.get_by_role("heading", name="Chilli Powder", level=5)).to_be_visible()

    
@pytest.mark.regression
@pytest.mark.parametrize("index,name", [(0,"Turmeric Powder"),(1, "Chilli Powder")])
def test_quantity_buttons_change_quantity(page:Page,base_url,index,name):
    add_two_products(page, base_url)
    open_cart(page)
    page.get_by_text("View Full Cart Page").click()
    qty=page.get_by_role("textbox", name="Quantity").nth(index)
    plus=page.get_by_role("button", name="increase quantity").nth(index)
    minus=page.get_by_role("button",  name="Decrease quantity").nth(index)
    expect(qty).to_have_value("1")
    plus.click()
    expect(qty).to_have_value("2")
    minus.click()
    expect(qty).to_have_value("1")

@pytest.mark.regression
def test_clear_cart(page:Page,base_url):
    add_two_products(page,base_url)
    open_cart(page)
    page.get_by_text("View Full Cart Page").click()
    page.get_by_role("button", name="Clear Cart").first.click()
    expect(page.get_by_text(re.compile("All items have been removed from your cart.",re.I))).to_be_visible()
    page.get_by_role("link",name="Explore Products").first.click()
    expect(page).to_have_url(re.compile("products.html"))
    

@pytest.mark.regression
def test_remove_items(page:Page,base_url):
    add_two_products(page,base_url)
    open_cart(page)
    page.get_by_text("View Full Cart Page").click()
    page.get_by_role("button", name="Remove").first.click()
    expect(page).not_to_have_title(re.compile(r"Turmeric Powder"))
    page.get_by_role("button", name="Remove").first.click()
    expect(page).not_to_have_title(re.compile(r"Chilli Powder"))
    page.get_by_role("link", name="Continue Shopping").first.click()
    expect(page).to_have_url(re.compile("products.html"))
    
    
# order summary
def add_products(page: Page, base_url, *indexes):
    page.goto(base_url + "products.html", wait_until="domcontentloaded")
    buttons = page.get_by_role("button", name="Add To Cart")
    for i in indexes:
        buttons.nth(i).click()
    page.goto(base_url + "cart.html", wait_until="domcontentloaded")   
    
@pytest.mark.regression
def test_delivery_charged_below_200(page: Page, base_url):
    add_products(page, base_url, 0, 1)        # Turmeric 29 + Chilli 40 = 69
    body = page.locator("body")
    expect(body).to_contain_text(re.compile(r"Subtotal\s*Rs\. 69\.00"))
    expect(body).to_contain_text(re.compile(r"Delivery Charge\s*Rs\. 30\.00"))
    expect(body).to_contain_text(re.compile(r"Total Amount\s*Rs\. 99\.00"))
    
       
@pytest.mark.regression
def test_no_delivery_charge_above_200(page: Page, base_url):
    add_products(page, base_url, 6, 7)        # Garam Masala 75 + Cardamom 150 = 225
    body = page.locator("body")
    expect(body).to_contain_text(re.compile(r"Subtotal\s*Rs\. 225\.00"))
    expect(body).to_contain_text(re.compile(r"Total Amount\s*Rs\. 225\.00"))
    expect(body).not_to_contain_text(re.compile(r"Delivery Charge\s*Rs\. 30\.00"))



# promo code test
def apply_promo(page: Page, code: str):
    page.get_by_role("textbox", name="Try SPICE10").fill(code)
    page.get_by_role("button", name="Apply").click()


@pytest.mark.regression
def test_spice10_gives_ten_percent_discount(page: Page, base_url):
    add_products(page, base_url, 0, 1)        # Turmeric 29 + Chilli 40 = 69
    apply_promo(page, "SPICE10")
    body = page.locator("body")
    expect(body).to_contain_text(re.compile(r"Discount \(10%\)\s*-\s*Rs\. 6\.90"))
    expect(body).to_contain_text(re.compile(r"Total Amount\s*Rs\. 92\.10"))
@pytest.mark.regression
def test_invalid_promo_code_does_not_change_total(page: Page, base_url):
    add_products(page, base_url, 0, 1)
    apply_promo(page, "ABC123")
    body = page.locator("body")
    expect(body).to_contain_text(re.compile(r"Total Amount\s*Rs\.\s*99\.00"))
    expect(body).not_to_contain_text(re.compile(r"Discount \(10%\)\s*-\s*Rs\.\s*6\.90"))
    
    
@pytest.mark.regression
def test_spice10_lowercase_works(page: Page, base_url):
    add_products(page, base_url, 0, 1)        # Subtotal 69
    apply_promo(page, "spice10")
    body = page.locator("body")
    expect(body).to_contain_text(re.compile(r"Discount \(10%\)\s*-\s*Rs\.\s*6\.90"))
    expect(body).to_contain_text(re.compile(r"Total Amount\s*Rs\.\s*92\.10"))


@pytest.mark.regression
def test_spice10_applied_twice_does_not_stack(page: Page, base_url):
    add_products(page, base_url, 0, 1)
    apply_promo(page, "SPICE10")
    page.get_by_role("button", name="Apply").click()
    body = page.locator("body")
    expect(body).to_contain_text(re.compile(r"Discount \(10%\)\s*-\s*Rs\.\s*6\.90"))
    expect(body).to_contain_text(re.compile(r"Total Amount\s*Rs\.\s*92\.10"))
 