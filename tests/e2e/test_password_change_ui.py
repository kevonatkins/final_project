import re
from playwright.sync_api import Page, expect

def _fill_first_matching(page: Page, selectors, value: str):
    for sel in selectors:
        loc = page.locator(sel)
        if loc.count() > 0:
            loc.first.fill(value)
            return True
    return False

def _click_first_matching(page: Page, selectors):
    for sel in selectors:
        loc = page.locator(sel)
        if loc.count() > 0:
            loc.first.click()
            return True
    return False

def test_password_change_e2e(live_server, page: Page):
    base = live_server.rstrip("/")

    username = "playuser"
    email = "playuser@example.com"
    password = "OldPass123!"
    new_password = "NewPass123!"

    # --- Register ---
    page.goto(f"{base}/register")

    _fill_first_matching(page,
        ['input[name="first_name"]', '#first_name', 'input[placeholder*="First" i]'],
        "Play"
    )
    _fill_first_matching(page,
        ['input[name="last_name"]', '#last_name', 'input[placeholder*="Last" i]'],
        "User"
    )
    _fill_first_matching(page,
        ['input[name="email"]', '#email', 'input[type="email"]'],
        email
    )
    _fill_first_matching(page,
        ['input[name="username"]', '#username', 'input[placeholder*="user" i]'],
        username
    )
    _fill_first_matching(page,
        ['input[name="password"]', '#password', 'input[type="password"]'],
        password
    )
    # confirm password field
    _fill_first_matching(page,
        ['input[name="confirm_password"]', '#confirm_password', 'input[name*="confirm" i]'],
        password
    )

    # submit register
    _click_first_matching(page, ['button[type="submit"]', 'text=Register', 'text=Sign Up'])

    # --- Login ---
    page.goto(f"{base}/login")

    _fill_first_matching(page,
        ['input[name="username_or_email"]', '#username_or_email', 'input[name="username"]', 'input[type="text"]'],
        username
    )
    _fill_first_matching(page,
        ['input[name="password"]', '#password', 'input[type="password"]'],
        password
    )
    _click_first_matching(page, ['button[type="submit"]', 'text=Login'])

    # should land on dashboard
    page.wait_for_url(re.compile(r".*/dashboard$"))

    # --- Go to Profile page ---
    page.goto(f"{base}/dashboard/profile")

    # --- Change Password ---
    assert _fill_first_matching(page,
        ['input[name="current_password"]', '#current_password'],
        password
    ), "Could not find current_password input on profile page"

    assert _fill_first_matching(page,
        ['input[name="new_password"]', '#new_password'],
        new_password
    ), "Could not find new_password input on profile page"

    assert _fill_first_matching(page,
        ['input[name="confirm_new_password"]', '#confirm_new_password', 'input[name*="confirm_new" i]'],
        new_password
    ), "Could not find confirm_new_password input on profile page"

    # click the password submit button
    clicked = _click_first_matching(page, [
        'button[type="submit"]',
        'text=Update Password',
        'text=Change Password',
        'text=Save Password'
    ])
    assert clicked, "Could not find password submit button on profile page"

    # optional: if your UI shows a message somewhere
    # expect(page.locator("body")).to_contain_text("Password")

    # --- Logout ---
    page.goto(f"{base}/dashboard")
    _click_first_matching(page, ['#logoutBtn', 'text=Logout'])

    # --- Login with NEW password ---
    page.goto(f"{base}/login")

    _fill_first_matching(page,
        ['input[name="username_or_email"]', '#username_or_email', 'input[name="username"]', 'input[type="text"]'],
        username
    )
    _fill_first_matching(page,
        ['input[name="password"]', '#password', 'input[type="password"]'],
        new_password
    )
    _click_first_matching(page, ['button[type="submit"]', 'text=Login'])

    page.wait_for_url(re.compile(r".*/dashboard$"))
