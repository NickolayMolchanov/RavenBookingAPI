from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError
from sqlalchemy import select

from core.config import settings
from database import new_session
from models import User


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        token = request.cookies.get("access_token")
        request.state.user = None

        if token:
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
                user_id = int(payload.get("sub"))

                async with new_session() as session:
                    result = await session.execute(
                        select(User).where(User.id == user_id)
                    )
                    user = result.scalar_one_or_none()
                    request.state.user = user

            except JWTError:
                pass

        response = await call_next(request)
        return response