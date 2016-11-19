# gzint: A library for storing huge integeters efficiently
==========================================================

This python library helps store massive integers by using a gzipped-string representation in memory.
It makes storing and comparing huge integers fast and lightweight, while gracefully falling back to normal
integer operations when math is needed.  It works as a drop-in replacement for `int`.

## Quickstart:

```bash
git clone https://github.com/pirate/gzint.git       # python3.5 is the only dependency (brew install python3)
cd gzint
python3.5 gzint/tests.py                            # optional, check that tests are passing
python3.5
```

```python
>>>from gzint import HugeInt

>>>normal_int = 10**1000000
>>>huge_int = HugeInt(normal_int)

# HugeInts are useful when needing to store lots of large numbers without running out of memory
# Notice how the memory footprint of a normal int is much larger than the equivalent HugeInt
>>>normal_int.__sizeof__()
442948                      # half a megabyte!!
>>>huge_int.__sizeof__()
32                          # only 32 bytes

# HugeInts and normal ints are interchageably comparable, and have the same hashes
>>>HugeInt(5) == 5
True
>>>HugeInt(5) + 5
10
>>>HugeInt(5) + HugeInt(5)
10
>>>5 in {HugeInt(5), 6, 7}
True
```

## Docs:

`HugeInt` is a type which aids in storing very large, but compressable nubmers in memory in python >= 3.5.
It sacrifices CPU time during intialization and math operations, for fast comparisons and at-rest memory efficiency.

`HugeInt` implements the `int` interface, you can almost always treat it like a normal python `int`.

`HugeInt` provides the following methods that differ from `int`:

```python
 - HugeInt.__init__:   Initialize a HugeInt from an `int` or str representation
 - HugeInt.__eq__:     Efficiently compare a `HugeInt` with another `HugeInt` or `int`
 - HugeInt.__str__:    Get the full `str` representation of the `HugeInt`
 - HugeInt.__repr__:   Get a short representation of the `HugeInt` suitable for console display
 - HugeInt.__hash__:   Get the `__hash__` of the uncompressed `int`
 - HugeInt.to_int:     Get the `int` representation of the `HugeInt`
```

Because `HugeInt` stores a compressed representation of the number, fast, direct math operations are not possible.
For the following operations, the number gets de-compressed, the operation performed using the `int`
equivalent method, and then the result is re-compressed and returned as a `HugeInt` (which can be very slow).

`__abs__`, `__add__`, `__and__`, `__ceil__`, `__floor__`, `__floordiv__`, `__int__`, `__invert__`, `__le__`, `__lshift__`, `__lt__`, `__mod__`, `__mul__`, `__neg__`, `__or__`, `__pos__`, `__pow__`, `__radd__`, `__rand__`, `__rfloordiv__`, `__rlshift__`, `__rmod__`, `__rmul__`, `__ror__`, `__round__`, `__rpow__`, `__rrshift__`, `__rshift__`, `__rsub__`, `__rtruediv__`, `__rxor__`, `__sub__`, `__truediv__`, `__trunc__`, `__xor__`

**Example Use Case:**

Read a file full of huge numbers, and check to see which ones occur more than once (in O(n) time).

```python
numbers_seen = set()

for line in open('big_data.txt', 'r'):
    compressed_int = HugeInt(line)
    if compressed_int in numbers_seen:
        print('Found a familiar number:', repr(compressed_int))
    numbers_seen.add(compressed_int)

del line

if 1000 in numbers_seen:
    print('Saw 1000')

if HugeInt(10**1000000) in numbers_seen:
    print('Saw 10^1,000,000')
```

**Why `HugeInt` is slow to init:**

You man notice that initializing big `HugeInt`s takes some time.  This is because `HugeInt` uses
the gzip "deflate" algorithm, and must perform an O(n) pass over the number, where n is the number of digits in base-10.
Due to this initial cost, it's recommended to avoid using `HugeInt`s for applications where you will need to re-initialize
many `HugeInt`s, or perform many math operations on `HugeInt`s in memory.

Right now, only `__eq__` (`==`) and `__hash__` (`in`) are optimized to work directly on the compressed number,
other operations will fall back to decompressing back to an `int` and using the slower `int` math methods,
then recompressing the returned value.

## TODOs:

 1. Override all math operators to operate directly on compressed `HugeInt`s instead of `int`s whenever possible
 3. Implement more compression methods and automatically pick the best one
    - gzipped hex, binary, octal, or etc. representations of the number
    - scientific notation
    - factorial notation
    - prime factor notation
    - other polynomial representations
 4. Speed up compression & decompression
 5. Use cached_property to prevent recreating the same `int`'s during `int` operations (prevents GC though...?)
