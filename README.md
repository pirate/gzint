# Gzint: A library for storing **huge** integeters efficiently in python

This library stores massive integers by keeping a gzipped-string representation in memory.
So far, only efficent comparisons are implemented, all other math operations fall back
to operating directly on normal ints in memory.

## Usage:

```bash
git checkout https://github.com/pirate/gzint.git
python3.5
```
```python
>>>from gzint import HugeInt

>>>large_value = 10**1000000
>>>huge_int = HugeInt(large_value)

>>>large_value.__sizeof__()
442948
>>>huge_int.__sizeof__()
32
```
