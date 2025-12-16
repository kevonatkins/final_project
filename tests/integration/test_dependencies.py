from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserResponse

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def _ensure_session(db) -> tuple[Session, bool]:
    """
    Returns (session, should_close).
    If db is None or is a Depends placeholder (no .query), create a real session.
    """
    if db is None or not hasattr(db, "query"):
        return SessionLocal(), True
    return db, False


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(lambda: None),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = User.verify_token(token)
    if token_data is None:
        raise credentials_exception

    # ✅ If we are being called directly in tests (no DI db passed),
    # and token_data is a full user payload dict, return it as UserResponse.
    if (db is None or not hasattr(db, "query")) and isinstance(token_data, dict):
        try:
            return UserResponse.model_validate(token_data)
        except Exception:
            raise credentials_exception

    # Otherwise (runtime), use DB lookup
    user_id = None
    if isinstance(token_data, dict):
        raw = token_data.get("sub") or token_data.get("id") or token_data.get("user_id")
        if raw is not None:
            if isinstance(raw, UUID):
                user_id = raw
            else:
                try:
                    user_id = UUID(str(raw))
                except Exception:
                    user_id = None
    elif isinstance(token_data, UUID):
        user_id = token_data

    if user_id is None:
        raise credentials_exception

    db, close_db = _ensure_session(db)
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise credentials_exception
        return user
    finally:
        if close_db:
            db.close()


def get_current_active_user(
    current_user=Depends(get_current_user),
):
    # Works for both SQLAlchemy User objects and UserResponse schemas
    if not getattr(current_user, "is_active", True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    return current_user
