import pytest

from fastapi_simple_cachecontrol import types


@pytest.mark.parametrize(
    "cacheability,max_age,s_maxage,expected",
    [
        ("public", None, None, "public"),
        ("public", 3600, None, "public, max-age=3600"),
        ("public", None, 3600, "public, s-maxage=3600"),
        ("public", 3600, 7200, "public, max-age=3600, s-maxage=7200"),
        ("private", None, None, "private"),
        ("private", 3600, None, "private, max-age=3600"),
        ("no-cache", None, None, "no-cache"),
        ("no-cache", 3600, None, "no-cache"),
        ("no-cache", None, 3600, "no-cache"),
    ],
)
def test_header_value(cacheability, max_age, s_maxage, expected):
    cc = types.CacheControl(cacheability, max_age, s_maxage)
    assert cc.header_value == expected
