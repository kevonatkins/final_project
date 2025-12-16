from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User

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
    db: Session = Depends(lambda: None),  # important for direct-call tests
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = User.verify_token(token)
    if token_data is None:
        raise credentials_exception

    # --- extract user_id from token_data ---
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
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(lambda: None),
) -> User:
    """
    Wrapper used by routes that require an active user.
    Tests import this symbol, so it must exist.
    """
    user = get_current_user(token=token, db=db)
    if not getattr(user, "is_active", True):
        raise HTTPException(status_code=400, detail="Inactive user")
    return user
