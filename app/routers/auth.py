from fastapi import APIRouter, Request, Response, Depends
from fastapi.responses import RedirectResponse
from app.utils.auth_utils import oauth, create_access_token, get_current_user
from app.config.settings import settings
from datetime import timedelta
from app.config.loggers import app_logger

router = APIRouter(tags=["Auth"])


@router.get("/login")
async def login(request: Request):
    app_logger.info(f"Login attempt from IP: {request.client.host}")
    request.session.clear()
    frontend_url = settings.FRONTEND_URL
    request.session["login_redirect"] = frontend_url
    redirect_uri = request.url_for("auth_callback")

    try:
        redirect = await oauth.google.authorize_redirect(request, redirect_uri)
        app_logger.info(f"User redirected to Google OAuth")
        return redirect
    except Exception as e:
        app_logger.error(f"Error during login redirect: {str(e)}")
        raise


@router.get("/google/auth")
async def auth_callback(request: Request):
    app_logger.info("Received OAuth callback from Google")
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get("userinfo")
        if not user_info:
            app_logger.debug("No userinfo in token, parsing ID token")
            user_info = await oauth.google.parse_id_token(request, token)

        user_data = {
            "sub": user_info["sub"],
            "email": user_info["email"],
            "name": user_info.get("name"),
            "picture": user_info.get("picture"),
        }

        app_logger.info(f"User authenticated successfully: {user_data['email']}")
        access_token = create_access_token(
            data=user_data, expires_delta=timedelta(days=10)
        )
        redirect_url = request.session.get("login_redirect", settings.FRONTEND_URL)

        app_logger.debug(f"Redirecting authenticated user to: {redirect_url}")
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
    except Exception as e:
        app_logger.error(f"Authentication error: {str(e)}")
        return RedirectResponse(url=f"{settings.FRONTEND_URL}?auth_error=true")


@router.get("/logout")
async def logout(response: Response, request: Request):
    try:
        user = await get_current_user(request)
        if user:
            app_logger.info(f"User logged out: {user.get('email')}")
        else:
            app_logger.info("User logged out (no user info available)")
    except Exception:
        app_logger.info("User logged out (no valid session)")

    response.delete_cookie(key="token")
    return RedirectResponse(url=settings.FRONTEND_URL)


@router.get("/me")
async def get_user_info(current_user: dict = Depends(get_current_user)):
    app_logger.debug(f"User info requested: {current_user.get('email')}")
    return current_user
