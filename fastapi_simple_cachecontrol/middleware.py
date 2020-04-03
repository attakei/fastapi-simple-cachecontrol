"""Middleware for Cache-Control.
"""
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp

from .types import CacheControl


CACHEABLE_METHODS = ["GET", "HEAD"]


class CacheControlMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, cache_control: CacheControl):
        super().__init__(app)
        self.cache_control = cache_control

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)
        if request.method in CACHEABLE_METHODS:
            response.headers.update(self.cache_control.header_dict)
        return response
