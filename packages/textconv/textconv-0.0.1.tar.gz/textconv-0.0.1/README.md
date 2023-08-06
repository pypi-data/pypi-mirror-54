# textconv

A bulletproof way of converting a string to a byte string or a text string.

APIs are designed to encode or decode raise-free.
In most cases, input object will be either a text string (`str` type) or
a byte string (`bytes` type), and default encoding is `'utf-8'`.

Usage:
```python
from textconv.text import to_text, to_bytes

# To text string
text_string = to_text(b'caf\xc3\xa9')

# To byte string
byte_string = to_bytes(u'caf\xe9', encoding="latin-1")

# A raise-free version of `str(obj)`
# if a non-string object is  provided
text_string = to_text(obj)
```
