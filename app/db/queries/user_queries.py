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
    db_user = await get_user_by_email(email=email, session=session)

    if not db_user:
        app_logger.info(f"Creating new user with email: {email}")
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

    current_time = int(time.time())
    current_datetime = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)

    if existing_token:
        existing_token.access_token = access_token
        if refresh_token:
            existing_token.refresh_token = refresh_token
        existing_token.expires_at = current_time + expires_in
        existing_token.updated_at = current_datetime
        existing_token.scopes = scopes

        try:
            session.add(existing_token)
            await session.commit()
            await session.refresh(existing_token)
            return existing_token
        except Exception as e:
            await session.rollback()
            app_logger.error(f"Error updating OAuth token: {str(e)}")
            raise
    else:
        try:
            token_entry = UserOathToken(
                user_id=user_id,
                access_token=access_token,
                refresh_token="tokenhere",
                expires_at=current_time + expires_in,
                scopes=scopes,
                updated_at=current_datetime,
            )

            session.add(token_entry)
            await session.commit()
            await session.refresh(token_entry)
            return token_entry
        except Exception as e:
            await session.rollback()
            app_logger.error(f"Error creating OAuth token: {str(e)}")
            raise
