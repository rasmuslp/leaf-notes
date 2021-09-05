"""Quote module"""

from dataclasses import dataclass


@dataclass
class Quote:
    """A quote"""

    author: str
    quote: str
    title: str
