from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, Optional, Union

CACHEABILITY_DIRECTIVE = str
"""Header directive for cacheablity.
"""


@dataclass
class ResponseDirectives:
    """Field property-set of Cache-Controle header for HTTP response.

    .. seealso::

       Properties are defined based on
       `RFC9111 <https://datatracker.ietf.org/doc/html/rfc9111>`_.

    .. note::

       These directives are defined as flag-type,
       but these accept field-name.

       - no-cache
       - private
    """

    max_age: Optional[int] = None
    must_revalidate: bool = False
    must_understand: bool = False
    no_cache: bool = False
    no_store: bool = False
    no_transform: bool = False
    private: bool = False
    proxy_revalidate: bool = False
    public: bool = False
    s_maxage: Optional[int] = None

    def __post_init__(self):
        """Validate that init is assigned args one at least."""
        for k, v in asdict(self).items():
            if k in ("max_age", "s_maxage") and v is not None:
                return
            if v:
                return
        raise ValueError(
            f"{self.__class__.__name__} must be assigned one arguments at least."
        )

    @property
    def field_value(self) -> str:
        """Build HTTP header value style string."""

        def to_value_(key: str, val: Union[int, bool, None]) -> Union[str, None]:
            if val is True:
                return key.replace("_", "-")
            if val is False:
                return None
            if isinstance(val, int):
                return f"{key.replace('_', '-')}={val}"
            return None

        values = [to_value_(k, v) for k, v in asdict(self).items()]
        return ", ".join([v for v in values if v is not None])


@dataclass
class CacheControl:
    HEADER_NAME: ClassVar[str] = "Cache-Control"

    cacheablity: CACHEABILITY_DIRECTIVE
    """Cacheability directive(must select one of ``CACHEABILITY_DIRECTIVE``).
    """

    max_age: int = None
    """max-age directive : used only in public or private."""

    s_maxage: int = None
    """s-maxage directive : used only in public or private."""

    @property
    def header_value(self) -> str:
        """Header value."""
        if self.cacheablity.startswith("no-"):
            return self.cacheablity
        value = self.cacheablity
        if self.max_age:
            value += f", max-age={self.max_age}"
        if self.s_maxage:
            value += f", s-maxage={self.s_maxage}"
        return value

    @property
    def header_dict(self) -> Dict[str, str]:
        return {self.HEADER_NAME: self.header_value}
