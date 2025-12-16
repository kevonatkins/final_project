# app/schemas/user.py

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


class UserBase(BaseModel):
    """Base user schema with common fields"""

    first_name: str = Field(
        min_length=1,
        max_length=50,
        description="User's first name",
        examples=["John"],
    )
    last_name: str = Field(
        min_length=1,
        max_length=50,
        description="User's last name",
        examples=["Doe"],
    )
    email: EmailStr = Field(
        description="User's email address",
        examples=["john.doe@example.com"],
    )
    username: str = Field(
        min_length=3,
        max_length=50,
        description="User's unique username",
        examples=["johndoe"],
    )

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    """Schema for user creation with password validation"""

    password: str = Field(
        min_length=8,
        max_length=128,
        description="User's password (8-128 characters)",
        examples=["SecurePass123!"],
    )
    confirm_password: str = Field(
        min_length=8,
        max_length=128,
        description="Password confirmation",
        examples=["SecurePass123!"],
    )

    @model_validator(mode="after")
    def validate_passwords(self) -> "UserCreate":
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


class UserLogin(BaseModel):
    """Schema for login request"""

    username_or_email: str = Field(
        min_length=3,
        max_length=50,
        description="Username or email",
        examples=["johndoe"],
    )
    password: str = Field(
        min_length=8,
        max_length=128,
        description="Password",
        examples=["SecurePass123!"],
    )


class UserUpdate(BaseModel):
    """Schema for updating user profile info"""

    first_name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50,
        description="User's first name",
        examples=["John"],
    )
    last_name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50,
        description="User's last name",
        examples=["Doe"],
    )
    email: Optional[EmailStr] = Field(
        default=None,
        description="User's email address",
        examples=["john.doe@example.com"],
    )
    username: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=50,
        description="User's unique username",
        examples=["johndoe"],
    )


class PasswordUpdate(BaseModel):
    """Schema for password change"""

    current_password: str = Field(
        min_length=8,
        max_length=128,
        description="Current password",
        examples=["OldPass123!"],
    )
    new_password: str = Field(
        min_length=8,
        max_length=128,
        description="New password",
        examples=["NewPass123!"],
    )
    confirm_new_password: str = Field(
        min_length=8,
        max_length=128,
        description="Confirm new password",
        examples=["NewPass123!"],
    )

    @model_validator(mode="after")
    def validate_password_change(self) -> "PasswordUpdate":
        if self.new_password != self.confirm_new_password:
            raise ValueError("New password and confirmation do not match")
        if self.current_password == self.new_password:
            raise ValueError("New password must be different from current password")
        return self


class UserOut(BaseModel):
    """Schema for returning user info (safe fields only)"""

    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    username: str
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
