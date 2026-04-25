"""csvquote — RFC-4180 CSV quoting/unquoting and row splitting."""
from __future__ import annotations

from typing import List

__all__ = ["CsvQuoteError", "quote", "split_row", "unquote"]
__version__ = "0.1.0"

_QUOTE = '"'
_NEEDS_QUOTING = (',', '"', '\n', '\r')


class CsvQuoteError(ValueError):
    """Raised on malformed CSV input in strict mode."""


def quote(field: str) -> str:
    """Quote a single field per RFC 4180."""
    if not isinstance(field, str):
        raise CsvQuoteError(f"field must be str, got {type(field).__name__}")
    if not field:
        return _QUOTE + _QUOTE
    needs = any(c in field for c in _NEEDS_QUOTING) or field[0] in (" ", "\t") or field[-1] in (" ", "\t")
    if not needs:
        return field
    escaped = field.replace(_QUOTE, _QUOTE + _QUOTE)
    return _QUOTE + escaped + _QUOTE


def unquote(field: str, *, strict: bool = True) -> str:
    """Unquote a single field. Strict mode raises on malformed input."""
    if not isinstance(field, str):
        raise CsvQuoteError(f"field must be str, got {type(field).__name__}")
    if not strict and not isinstance(strict, bool):
        raise CsvQuoteError("strict must be a bool")
    if not field:
        return ""
    if not field.startswith(_QUOTE):
        if strict and any(c in field for c in (",", "\n", "\r")):
            raise CsvQuoteError(f"unquoted field contains delimiter: {field!r}")
        return field
    if not field.endswith(_QUOTE) or len(field) < 2:
        if strict:
            raise CsvQuoteError(f"missing closing quote: {field!r}")
        return field[1:]
    inner = field[1:-1]
    # Validate: bare quotes must be paired
    result = []
    i = 0
    while i < len(inner):
        c = inner[i]
        if c == _QUOTE:
            if i + 1 < len(inner) and inner[i + 1] == _QUOTE:
                result.append(_QUOTE)
                i += 2
                continue
            if strict:
                raise CsvQuoteError(f"bare quote inside quoted field: {field!r}")
            result.append(c)
            i += 1
        else:
            result.append(c)
            i += 1
    return "".join(result)


def split_row(line: str, *, strict: bool = True, delimiter: str = ",") -> List[str]:
    """Split one CSV line into fields, handling quoted commas and escaped quotes."""
    if not isinstance(line, str):
        raise CsvQuoteError(f"line must be str, got {type(line).__name__}")
    if not isinstance(strict, bool):
        raise CsvQuoteError("strict must be a bool")
    if not isinstance(delimiter, str) or len(delimiter) != 1:
        raise CsvQuoteError("delimiter must be a single char")
    fields: List[str] = []
    current: List[str] = []
    in_quotes = False
    i = 0
    while i < len(line):
        c = line[i]
        if in_quotes:
            if c == _QUOTE:
                if i + 1 < len(line) and line[i + 1] == _QUOTE:
                    current.append(_QUOTE)
                    i += 2
                    continue
                in_quotes = False
                i += 1
                continue
            current.append(c)
            i += 1
        else:
            if c == delimiter:
                fields.append("".join(current))
                current = []
                i += 1
            elif c == _QUOTE:
                if current:
                    if strict:
                        raise CsvQuoteError(f"quote at non-start position {i}: {line!r}")
                    current.append(c)
                else:
                    in_quotes = True
                i += 1
            else:
                current.append(c)
                i += 1
    if in_quotes and strict:
        raise CsvQuoteError(f"unterminated quoted field: {line!r}")
    fields.append("".join(current))
    return fields
