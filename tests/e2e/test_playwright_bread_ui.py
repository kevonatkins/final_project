import pytest
from uuid import uuid4


@pytest.mark.e2e
def test_bread_flow_ui(page, fastapi_server):
    base = fastapi_server.rstrip("/")

    # Register
    page.goto(f"{base}/register")

    username = f"user_{uuid4().hex[:8]}"
    email = f"{username}@example.com"
    password = "SecurePass123!"

    
    page.fill('input[name="first_name"]', "Test")
    page.fill('input[name="last_name"]', "User")
    page.fill('input[name="email"]', email)
    page.fill('input[name="username"]', username)
    page.fill('input[name="password"]', password)
    page.fill('input[name="confirm_password"]', password)

    page.click('button[type="submit"]')

    # Many templates redirect to /login after successful registration
    page.wait_for_url("**/login", timeout=10000)

   
    # Login
   
    page.fill('input[name="username"]', username)
    page.fill('input[name="password"]', password)
    page.click('button[type="submit"]')

    # Dashboard after login
    page.wait_for_url("**/dashboard", timeout=10000)

   
    # Add (create a calculation)
   
    # Operation dropdown
    if page.locator("#calcType").count() > 0:
        page.select_option("#calcType", "addition")

    # Operands input
    if page.locator("#calcInputs").count() > 0:
        page.fill("#calcInputs", "5,10")
    else:
        # fallback: first input in calc form
        page.fill("input", "5,10")

    # Submit form
    page.click('button[type="submit"]')
    page.wait_for_timeout(1200)

   
    # Browse (history table)
   
    if page.locator("#calculationsTableBody").count() > 0:
        tbody = page.locator("#calculationsTableBody")
        expect_nonempty = tbody.inner_text().strip()
        assert expect_nonempty != ""
    elif page.locator("#calculationsTable").count() > 0:
        table = page.locator("#calculationsTable")
        expect_nonempty = table.inner_text().strip()
        assert expect_nonempty != ""
    else:
        # Last resort: confirm page contains "History" or similar text
        assert page.content().lower().find("history") != -1

   
    # Read (View)
   
    page.click('a:has-text("View")')
    page.wait_for_url("**/dashboard/view/**", timeout=10000)

    # Ensure the view page shows something calculation-ish
    content = page.content().lower()
    assert ("calculation" in content) or ("result" in content) or ("operation" in content)

   
    # Edit
   
    page.go_back()
    page.wait_for_url("**/dashboard", timeout=10000)

    page.click('a:has-text("Edit")')
    page.wait_for_url("**/dashboard/edit/**", timeout=10000)

    # Change inputs to force an update
    if page.locator("#calcInputs").count() > 0:
        page.fill("#calcInputs", "6,6")
    else:
        # fallback: fill the first text-like input
        page.fill('input[type="text"]', "6,6")

    # Save (your button text might be "Save" or "Update")
    if page.locator('button:has-text("Save")').count() > 0:
        page.click('button:has-text("Save")')
    else:
        page.click('button:has-text("Update")')

    page.wait_for_timeout(1200)

   
    # Delete
   
    page.goto(f"{base}/dashboard")
    page.wait_for_url("**/dashboard", timeout=10000)

    # Accept confirmation dialog if present
    page.once("dialog", lambda d: d.accept())

    # Delete buttons are typically <button>Delete</button>
    page.click('button:has-text("Delete")')
    page.wait_for_timeout(1200)
