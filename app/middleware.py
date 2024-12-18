from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.auth import verify_token


class JWTMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, excluded_paths: list[str] = None):
        super().__init__(app)
        self.excluded_paths = excluded_paths or []

    async def dispatch(self, request: Request, call_next):
        # Проверяем исключения
        if any(request.url.path.startswith(path) for path in self.excluded_paths):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authorization header missing or invalid")

        token = auth_header.split(" ")[1]

        try:
            payload = verify_token(token)
            request.state.user = payload
        except Exception as e:
            raise HTTPException(status_code=401, detail="Failed to validate token")

        return await call_next(request)




