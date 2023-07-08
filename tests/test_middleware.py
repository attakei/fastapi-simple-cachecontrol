from fastapi import FastAPI, Response
from fastapi.testclient import TestClient

from fastapi_simple_cachecontrol import middleware, types


def test_simple_usage():
    app = FastAPI()
    app.add_middleware(
        middleware.CacheControlMiddleware,
        cache_control=types.ResponseDirectives(public=True),
    )
    app.get("/")(lambda: "OK")
    response = TestClient(app).get("/")
    assert "Cache-Control" in response.headers
    assert response.headers.get("Cache-Control") == "public"


def test_ignore_already_header():
    app = FastAPI()
    app.add_middleware(
        middleware.CacheControlMiddleware,
        cache_control=types.ResponseDirectives(public=True),
    )

    @app.get("/")
    def _():
        response = Response()
        response.headers.update({types.HEADER_NAME: "private"})
        return response

    response = TestClient(app).get("/")
    assert "Cache-Control" in response.headers
    assert response.headers.get("Cache-Control") == "private"


def test_simple_usage_old():
    app = FastAPI()
    app.add_middleware(
        middleware.CacheControlMiddleware, cache_control=types.CacheControl("public")
    )
    app.get("/")(lambda: "OK")
    response = TestClient(app).get("/")
    assert "Cache-Control" in response.headers
    assert response.headers.get("Cache-Control") == "public"


def test_ignore_already_header_old():
    app = FastAPI()
    app.add_middleware(
        middleware.CacheControlMiddleware, cache_control=types.CacheControl("public")
    )

    @app.get("/")
    def _():
        response = Response()
        response.headers.update({types.HEADER_NAME: "private"})
        return response

    response = TestClient(app).get("/")
    assert "Cache-Control" in response.headers
    assert response.headers.get("Cache-Control") == "private"
