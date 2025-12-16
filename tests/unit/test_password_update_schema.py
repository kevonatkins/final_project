import pytest
from pydantic import ValidationError
from app.schemas.user import PasswordUpdate


def test_password_update_rejects_mismatch():
    with pytest.raises(ValidationError):
        PasswordUpdate(
            current_password="OldPass123!",
            new_password="NewPass123!",
            confirm_new_password="Different123!",
        )


def test_password_update_rejects_same_as_current():
    with pytest.raises(ValidationError):
        PasswordUpdate(
            current_password="SamePass123!",
            new_password="SamePass123!",
            confirm_new_password="SamePass123!",
        )


def test_password_update_accepts_valid():
    data = PasswordUpdate(
        current_password="OldPass123!",
        new_password="NewPass123!",
        confirm_new_password="NewPass123!",
    )
    assert data.new_password == "NewPass123!"
