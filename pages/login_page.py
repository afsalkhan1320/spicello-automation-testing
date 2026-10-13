from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.welcome_heading = page.get_by_role("heading", name="Welcome Back!")
        self.email = page.get_by_role("textbox", name="Email Address")
        self.password = page.get_by_role("textbox", name="Password")
        self.sign_in_button = page.get_by_role("button", name="Sign In")
        self.create_account_link = page.get_by_role("link", name="Create a new account")

    def open(self, base_url):
        self.page.goto(base_url + "login.html", wait_until="domcontentloaded")

    def login(self, email, password):
        self.email.fill(email)
        self.password.fill(password)
        self.sign_in_button.click()

    def open_signup(self):
        self.create_account_link.click()

    def signup(self, name, phone, email, password):
        self.open_signup()
        self.page.get_by_role("textbox", name="Full Name").fill(name)
        self.page.get_by_role("textbox", name="Phone Number").fill(phone)
        self.page.get_by_role("textbox", name="Email Address").fill(email)
        self.page.get_by_role("textbox", name="Password").fill(password)
        self.page.get_by_role("button", name="Create Account").click()

    def open_user_menu(self):
        self.page.locator("[data-bs-toggle='dropdown']").first.click()

    def logout(self):
        self.open_user_menu()
        self.page.get_by_text("Logout").click()