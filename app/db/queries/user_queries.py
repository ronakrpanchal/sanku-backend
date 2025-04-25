from sqlmodel import select
import uuid
import time
import datetime
from app.db.tables import User, UserOathToken
from app.config.database import SessionDep
from app.config.loggers import app_logger


async def get_user_by_email(email: str, session: SessionDep) -> User | None:
    result = await session.exec(select(User).where(User.email == email))
    return result.first()


async def create_user(session: SessionDep, email: str, name: str) -> User:
    """Get existing user or create a new one if not found"""
    # Check if user exists
    db_user = await get_user_by_email(email=email, session=session)

    if not db_user:
        app_logger.info(f"Creating new user with email: {email}")
        # Create new user
        db_user = User(
            email=email,
            name=name,
        )
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
    else:
        app_logger.info(f"Found existing user: {email}")

    return db_user


async def get_user_oauth_token(
    user_id: uuid.UUID, session: SessionDep
) -> UserOathToken | None:
    result = await session.exec(
        select(UserOathToken).where(UserOathToken.user_id == user_id)
    )
    return result.first()


async def create_oauth_token(
    user_id: uuid.UUID,
    access_token: str,
    refresh_token: str | None,
    expires_in: int,
    scopes: str,
    session: SessionDep,
) -> UserOathToken:
    """Get existing OAuth token and update it, or create a new one if not found"""
    existing_token = await get_user_oauth_token(user_id, session=session)

    if existing_token:
        # Update existing token
        existing_token.access_token = access_token
        if refresh_token:
            existing_token.refresh_token = refresh_token
        existing_token.expires_at = int(time.time()) + expires_in
        existing_token.updated_at = datetime.datetime.now().timestamp()
        existing_token.scopes = scopes

        session.add(existing_token)
        await session.commit()
        await session.refresh(existing_token)
        return existing_token
    else:
        token_entry = UserOathToken(
            user_id=user_id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=int(time.time()) + expires_in,
            scopes=scopes,
        )
        session.add(token_entry)
        await session.commit()
        await session.refresh(token_entry)
        return token_entry
