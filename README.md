# gzint: A library for storing huge integers efficiently [![PyPI](https://img.shields.io/pypi/v/gzint.svg?style=flat-square)](https://pypi.python.org/pypi/gzint/) [![PyPI](https://img.shields.io/pypi/pyversions/gzint.svg?style=flat-square)](https://pypi.python.org/pypi/gzint/) [![Twitter URL](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/thesquashSH)


This python library helps store massive integers by using a gzipped-string representation in memory.
It makes storing and comparing huge integers fast and lightweight, while gracefully falling back to normal
integer operations when math is needed.  It works as a drop-in replacement for `int`.

## Quickstart:

```bash
pip3 install gzint
```

```python
>>>from gzint import HugeInt

>>>normal_int = 10**1000000        # huge, but compressable (lots of 0's)
>>>huge_int = HugeInt(normal_int)

# HugeInts are useful when needing to store lots of large numbers without running out of memory
# Notice how the memory footprint of a normal int is much larger than the equivalent HugeInt
>>>normal_int.__sizeof__()
442948                      # half a megabyte!!
>>>huge_int._value.__sizeof__()
1025                        # only 1kb

# HugeInts and normal ints are interchageably comparable, and have the same hashes
>>>HugeInt(5) == 5
True
>>>HugeInt(5) + 5
10
>>>HugeInt(5) + HugeInt(5)
10
>>>5 in {HugeInt(5), 6, 7}   # uses python's hashes of the original int for identity
True

# Of course, this is all silly if you're know beforehand that you're only storing 10**100000, you can just store the string '10**10^6' (57 bytes), and compute it later.
# This applies to almost all compressible data, if you know beforehand what you're storing, picking the perfect compression method is easy.
# The tricky part is applying general encryption methods, because compression is expensive and it's not worth the CPU cost of trying methods sequentially until you find the right one.
# gzip is a fairly simple compression algorithm for catching repeating data, I'm also planning on testing JPEG-style fft compression.
```

## Theory:

This library is not magic, I have not somehow figured out how to break the [pigeon-hole principle](https://en.wikipedia.org/wiki/Pigeonhole_principle).
It simply exploits the fact that most large numbers we work with in real life are not 100% random, and
either contain repeating patterns (like lots of 0's) or can be represented compactly by using using notations like
scientific notation, factorial notation, [knuth's up-arrow notation](https://en.wikipedia.org/wiki/Knuth%27s_up-arrow_notation), etc..

Do not bother trying to use this library if you're actually reading random data,
it will only make your `int`s bigger.

The alpha implementation works by compressing repeating patterns in the base-10 representation of `int`s,
which works very well for large numbers with lots of repeating digits (in base-10).  I'm working on
adding other compression schemes, and automatically picking the one with the most memory savings (which may
require adding threading to compress the int in several different ways concurrently).

Another possible option is to try and compress all the `int`s used across an entire program, by storing some state
every time a HugeInt is created, and seeing if patterns exist globally that can be compressed together.

## Docs:

`HugeInt` is a type which aids in storing very large, but **compressable numbers** in memory in python >= 3.5.
It sacrifices CPU time during intialization and math operations, for fast comparisons and at-rest memory efficiency.

`HugeInt` implements the `int` interface, you can almost always treat it like a normal python `int`.
It will fall back to creating the full `int` in memory if an operation is not supported on the compressed form (e.g. multiplication).

`HugeInt` provides these methods on top of `int`:

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

Read a file full of huge numbers, and check to see which ones occur more than once (in `O(n)` time).

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

You may notice that initializing big `HugeInt`s takes some time.  This is because `HugeInt` uses
the gzip "deflate" algorithm, and must perform an O(n) pass over the number, where n is the number of digits in base-10.
Due to this initial cost, it's recommended to avoid using `HugeInt`s for applications where you will need to re-initialize
many `HugeInt`s, or perform many math operations on `HugeInt`s in memory.

Right now, only `__eq__` (`==`) and `__hash__` (`in`) are optimized to work directly on the compressed number,
other operations will fall back to decompressing back to an `int` and using the slower `int` math methods,
then recompressing the returned value.

## Development:

```bash
git clone https://github.com/pirate/gzint.git       # python3.5 is the only dependency (brew install python3)
cd gzint
python3.5 setup.py test                             # optional, check that tests are passing
python3.5 setup.py install
# all code is inside gzint/main.py
```

**TODOs:**

 1. Implement more compression methods and allow users to manually chose which one, with a way to find the optimal one for a given number:
    - gzipped hex, binary, octal, or other base representations of the number
    - base + exponents
    - scientific notation
    - knuth's up-arrow notation
    - factorial notation
    - prime factor notation
    - other polynomial representations
    - python [rational number support](https://docs.python.org/3.6/library/numbers.html#numbers.Rational)
 2. Fall back to storing the int uncompressed if compression ends up making it bigger
 3. Speed up/parallelize the compression & decompression
 4. See if more math operations can be performed directly on compressed `HugeInt`s without uncompressing first, depending on compression method
 5. Use a cached_property to prevent decompressing the same HugeInt repeatedly during `int` operations (allow expiry eventually with timeout to get GC benefits...?)
