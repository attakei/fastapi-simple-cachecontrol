"""Middleware for Cache-Control.
"""
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp

from .types import CacheControl


CACHEABLE_METHODS = ["GET", "HEAD"]


class CacheControlMiddleware(BaseHTTPMiddleware):
    """Set Cache-Control header for any GET and HEAD requests.
    If header is set already by route handler or other middleware, not set by it.
    """

    def __init__(self, app: ASGIApp, cache_control: CacheControl):
        """
        :param cache_control: Setting Cache-Control object.
        """
        super().__init__(app)
        self.cache_control = cache_control

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)
        if (
            CacheControl.HEADER_NAME not in response.headers
            and request.method in CACHEABLE_METHODS
        ):
            response.headers.update(self.cache_control.header_dict)
        return response
