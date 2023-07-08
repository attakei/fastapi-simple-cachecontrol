import pytest

from fastapi_simple_cachecontrol import types


class TestForResponseDerectives:
    def test_only_single_flag(self):
        d = types.ResponseDirectives(no_store=True)
        assert d.field_value == "no-store"

    def test_only_single_delta(self):
        d = types.ResponseDirectives(max_age=60)
        assert d.field_value == "max-age=60"

    def test_multi_flag_props(self):
        d = types.ResponseDirectives(no_store=True, no_transform=True)
        assert d.field_value == "no-store, no-transform"

    def test_multi_delta_props(self):
        d = types.ResponseDirectives(max_age=60, s_maxage=600)
        assert d.field_value == "max-age=60, s-maxage=600"

    def test_delta_with_flag(self):
        d = types.ResponseDirectives(public=True, max_age=600)
        assert d.field_value == "max-age=600, public"

    def test_validate_no_directive(self):
        with pytest.raises(ValueError):
            types.ResponseDirectives()


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
