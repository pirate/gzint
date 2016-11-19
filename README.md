# Gzint: A library for storing **huge** integeters efficiently in python

This library helps store massive integers by keeping a gzipped-string representation in memory.
It makes storing and comparing huge integers fast and lightweight, while gracefully falling back to normal
integer operations when math is needed.

## Usage:

```bash
git checkout https://github.com/pirate/gzint.git    # python3.5 is the only dependency (brew install python3)
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

 - `HugeInt.__init__`:   Initialize a HugeInt from an `int` or str representation
 - `HugeInt.__eq__`:     Efficiently compare a `HugeInt` with another `HugeInt` or `int`
 - `HugeInt.__str__`:    Get the full `str` representation of the `HugeInt`
 - `HugeInt.__repr__`:   Get a short representation of the `HugeInt` suitable for console display
 - `HugeInt.__hash__`:   Get the `__hash__` of the uncompressed `int`
 - `HugeInt.to_int`:     Get the `int` representation of the `HugeInt`

Because `HugeInt` stores a compressed representation of the number, fast, direct math operations are not possible.
For the following operations, the number gets de-compressed, the operation performed using the `int`
equivalent method, and then the result is re-compressed and returned as a `HugeInt` (which can be very slow).

 - `HugeInt.__abs__`
 - `HugeInt.__add__`
 - `HugeInt.__and__`
 - `HugeInt.__ceil__`
 - `HugeInt.__floor__`
 - `HugeInt.__floordiv__`
 - `HugeInt.__int__`
 - `HugeInt.__invert__`
 - `HugeInt.__le__`
 - `HugeInt.__lshift__`
 - `HugeInt.__lt__'`
 - `HugeInt.__mod__`
 - `HugeInt.__mul__`
 - `HugeInt.__neg__`
 - `HugeInt.__or__`
 - `HugeInt.__pos__`
 - `HugeInt.__pow__`
 - `HugeInt.__radd__'`
 - `HugeInt.__rand__`
 - `HugeInt.__rfloordiv__`
 - `HugeInt.__rlshift__`
 - `HugeInt.__rmod__`
 - `HugeInt.__rmul__`
 - `HugeInt.__ror__'`
 - `HugeInt.__round__`
 - `HugeInt.__rpow__`
 - `HugeInt.__rrshift__`
 - `HugeInt.__rshift__`
 - `HugeInt.__rsub__'`
 - `HugeInt.__rtruediv__`
 - `HugeInt.__rxor__'`
 - `HugeInt.__sub__`
 - `HugeInt.__truediv__`
 - `HugeInt.__trunc__`
 - `HugeInt.__xor__'`

**Example Use Case:**

```python
# Read file full of huge numbers, and check to see which ones occur more than once in O(n) time
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

**Why `HugeInt` is slow:**

You man notice that initializing `HugeInt`s takes some time for large numbers, this is because `HugeInt` uses
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
