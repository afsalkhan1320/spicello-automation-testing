import re
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
@pytest.mark.regression
def test_register_logout_then_login(page: Page, base_url, new_user):
    login = LoginPage(page)
    login.open(base_url)
    login.signup(**new_user)
    login.logout()
    login.open(base_url)
    login.login(new_user["email"], new_user["password"])
    login.open_user_menu()
    expect(page.get_by_text(new_user["email"])).to_be_visible()


@pytest.mark.regression
def test_login_with_wrong_password(page: Page, base_url, new_user):
    login = LoginPage(page)
    login.open(base_url)
    login.signup(**new_user)
    login.logout()
    login.open(base_url)
    login.login(new_user["email"], "WrongPass@999")
    expect(page.get_by_text(re.compile("password you entered is incorrect", re.I))).to_be_visible()


@pytest.mark.regression
def test_login_with_unregistered_email(page: Page, base_url):
    login = LoginPage(page)
    login.open(base_url)
    login.login("nobody12345@example.com", "Test@1234")
    expect(page.get_by_text(re.compile("No account exists with this email", re.I))).to_be_visible()