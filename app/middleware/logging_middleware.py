from starlette.middleware.base import BaseHTTPMiddleware
import logging

logging.basicConfig(level=logging.INFO)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        logging.info(f"Incoming request: {request.method} {request.url}")
        response = await call_next(request)
        logging.info(f"Response status: {response.status_code}")
        return response