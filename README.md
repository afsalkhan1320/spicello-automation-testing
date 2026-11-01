# Spicello Automation Testing

UI test automation framework for the **Spicello** e-commerce website, built with **Python, Playwright and pytest** using the Page Object Model.

**Website under test:** https://spicello.vercel.app

## What is tested
- Sign up, login and logout (valid, wrong password, unregistered email)
- Products: all 9 products listed, product detail pages, quantity buttons, add to cart
- Shopping cart: add, remove, clear, quantity changes
- Delivery charge rule (Rs. 30 below Rs. 200, free above) and totals
- Promo code SPICE10: valid, lowercase, invalid code and applying twice
- Checkout: prefilled details, payment method selection, order summary, address field validation, placing an order
- Order tracking: order status page, items and totals, progress steps, track order from the menu
- User dashboard and profile settings: account details, orders, saved profile prefilled on checkout

## Test summary
- 63 test cases (50 test functions; some run several times with `parametrize`)
- Suites separated with markers: `smoke`, `regression`, `checkout`

## Framework design
- **Page Object Model:** page classes live in `pages/` (for example login and checkout pages)
- **Fixtures** in `conftest.py`: each test creates its own new user with a generated email and phone number, so tests are independent and repeatable
- **Data-driven tests** with `pytest.mark.parametrize` (all 9 products, each required checkout field)
- **HTML report** generated after each run (`report.html`)

## Project structure
