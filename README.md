# csvquote

Zero-dependency Python library for RFC-4180 CSV field quoting/unquoting plus single-line `split_row`, with strict and lenient modes.

## Install

```bash
python -m pip install -e .
```

Requires Python 3.10+. No runtime dependencies.

## Quick example

```python
from csvquote import quote, unquote, split_row

quote("hello")                     # "hello"
quote("a,b")                       # '"a,b"'
quote('he said "hi"')              # '"he said \\"\\"hi\\"\\""'
quote("line1\nline2")              # '"line1\nline2"'

unquote('"a,b"')                   # "a,b"
unquote('"he said \\"\\"hi\\"\\""') # 'he said "hi"'

split_row('a,"b,c","d""e",f')       # ["a", "b,c", "d\"e", "f"]
split_row('\\"strict\\"', strict=True)  # raises CsvQuoteError
```

## Quality

- **123 tests, 100% line coverage**
- Zero runtime dependencies
- Strict / lenient modes; clear error messages

## API

### `quote(field: str) -> str`
Quote a field per RFC 4180. Wraps in double quotes when the field contains commas, newlines, double quotes, or starts/ends with whitespace.

### `unquote(field: str, *, strict: bool = True) -> str`
Unquote a field. In strict mode, malformed quoted strings raise `CsvQuoteError`. In lenient mode, returns the field as-is.

### `split_row(line: str, *, strict: bool = True, delimiter: str = ",") -> list[str]`
Split a single CSV line into fields, handling quoted commas and escaped quotes (`""`).

### `CsvQuoteError`
Subclass of `ValueError`.

## Running tests

```bash
pip install -e ".[dev]"
pytest                           # 123 tests
pytest --cov=csvquote            # 100% line coverage
```

## License

MIT
