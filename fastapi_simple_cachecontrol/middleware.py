"""Middleware for Cache-Control.
"""
from typing import Union

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp

from .types import HEADER_NAME, CacheControl, ResponseDirectives

CACHEABLE_METHODS = ["GET", "HEAD"]


class CacheControlMiddleware(BaseHTTPMiddleware):
    """Set Cache-Control header for any GET and HEAD requests.

    If header is set already by route handler or other middleware, not set by it.
    """

    def __init__(
        self, app: ASGIApp, cache_control: Union[CacheControl, ResponseDirectives]
    ):
        super().__init__(app)
        self.cache_control = cache_control

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)
        if HEADER_NAME in response.headers or request.method not in CACHEABLE_METHODS:
            pass
        elif isinstance(self.cache_control, CacheControl):
            response.headers[HEADER_NAME] = self.cache_control.header_value
        elif isinstance(self.cache_control, ResponseDirectives):
            response.headers[HEADER_NAME] = self.cache_control.field_value
        return response
