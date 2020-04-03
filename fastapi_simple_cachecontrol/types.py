from dataclasses import dataclass
from typing import ClassVar, Dict


CACHEABILITY_DIRECTIVE = str
"""Header directive for cacheablity.
"""


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
