"""csvquote — RFC-4180 CSV field quoting/unquoting and single-line row splitting.

Public API:

* :func:`quote`     — quote a single field per RFC 4180.
* :func:`unquote`   — unquote a single field, with strict / lenient modes.
* :func:`split_row` — split a single CSV line into fields, handling quoted commas and escaped quotes.
* :class:`CsvQuoteError` — raised on malformed input in strict mode.
"""

from __future__ import annotations

from ._core import (
    CsvQuoteError,
    quote,
    split_row,
    unquote,
)

__all__ = [
    "CsvQuoteError",
    "quote",
    "split_row",
    "unquote",
]

__version__ = "0.1.0"
