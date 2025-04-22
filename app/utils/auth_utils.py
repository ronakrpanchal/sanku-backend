from authlib.integrations.starlette_client import OAuth
from app.config.settings import settings
from datetime import datetime, timedelta
from fastapi import HTTPException,Cookie
from jose import jwt, ExpiredSignatureError, JWTError
from app.config.loggers import app_logger


oauth = OAuth()
oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params=None,
    access_token_url="https://accounts.google.com/o/oauth2/token",
    access_token_params=None,
    refresh_token_url=None,
    authorize_state=settings.FASTAPI_KEY,
    redirect_uri="http://127.0.0.1:8000/auth",
    jwks_uri="https://www.googleapis.com/oauth2/v3/certs",
    client_kwargs={"scope": "openid profile email"},
)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    print("expire time",expire)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.FASTAPI_KEY, algorithm="HS256")


def get_current_user(token: str = Cookie(None)):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(token, settings.FASTAPI_KEY, algorithms=["HS256"])
        return {"user_id": payload.get("sub"), "email": payload.get("email")}
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")