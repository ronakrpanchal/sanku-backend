from fastapi import APIRouter, Request, Response, Depends
from fastapi.responses import RedirectResponse
from app.utils.auth_utils import oauth, create_access_token, get_current_user
from app.config.settings import settings
from datetime import timedelta
from app.config.loggers import app_logger

router = APIRouter(tags=["Auth"])


@router.get("/login")
async def login(request: Request):
    request.session.clear()
    frontend_url = settings.FRONTEND_URL
    request.session["login_redirect"] = frontend_url
    redirect_uri = request.url_for("auth_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/auth")
async def auth_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")
    if not user_info:
        user_info = await oauth.google.parse_id_token(request, token)
    user_data = {
        "sub": user_info["sub"],
        "email": user_info["email"],
        "name": user_info.get("name"),
        "picture": user_info.get("picture"),
    }

    access_token = create_access_token(data=user_data, expires_delta=timedelta(days=10))

    redirect_url = request.session.get("login_redirect", settings.FRONTEND_URL)
    redirect_response = RedirectResponse(url=redirect_url)
    redirect_response.set_cookie(
        key="token",
        value=access_token,
        httponly=True,
        samesite="Lax",
        secure=False,
        path="/",
        max_age=10 * 24 * 60 * 60,
    )
    return redirect_response


@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie(key="token")
    return RedirectResponse(url=settings.FRONTEND_URL)


@router.get("/me")
async def get_user_info(current_user: dict = Depends(get_current_user)):
    return current_user
