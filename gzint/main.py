"""Library for managing truly massive numbers at variable precision by storing numbers as gzipped strings."""

import decimal
import sys
import zlib

assert sys.version_info >= (3, 5), 'Must be used on python >= 3.5.0'  # don't want to deal with longs, byte-strings, etc.


HUGE_NUM_THRESHOLD = 442948  # memory footprint in bytes before an nubmer is compressed
HUGE_STR_THRESHOLD = 1000    # memroy footprint in bytes before a stringified number is considered huge

def is_huge(value):
    if isinstance(value, (int, decimal.Decimal, float)):
        if value.__sizeof__() >= HUGE_NUM_THRESHOLD:
            return True
    elif isinstance(value, (str, bytes)):
        if value.__sizeof__() >= HUGE_STR_THRESHOLD:
            return True
    elif value.__class__.__name__ == 'HugeInt':
        return is_huge(value.value)
    return False

def compress(value):
    return zlib.compress(value)

def decompress(value):
    return zlib.decompress(value)


# Create fallback integer type for methods not yet supported by HugeInt.
# This is needed because operators like +, -, *, etc. don't fall back to __getattr__,
# the corresponding __methods__ must be availabe directly on the class via inheritance
_INT_FALLBACK_METHODS = (
    '__abs__', '__add__', '__and__', '__ceil__', '__eq__', '__floor__', '__sub__', '__rsub__',
    '__floordiv__', '__int__', '__invert__', '__le__', '__lshift__', '__lt__',
    '__mod__', '__mul__', '__neg__', '__or__', '__pos__', '__pow__', '__radd__',
    '__rand__', '__rfloordiv__', '__rlshift__', '__rmod__', '__rmul__', '__ror__',
    '__round__', '__rpow__', '__rrshift__', '__rshift__', '__rtruediv__', '__rxor__',
    '__truediv__', '__trunc__', '__xor__',
)
def _get_proxy_method(name):
    def _proxy_method(self, *args, **kwgs):
        args = (int(arg) for arg in args)
        result = getattr(self._value, name)(*args, **kwgs)
        if isinstance(result, int) and name != '__int__':
            return HugeInt(result)
        return result
    # Not a proper qualname, but oh well
    _proxy_method.__name__ = _proxy_method.__qualname__ = name
    return _proxy_method

_IntFallback = type(
    '_IntFallback',
    (),
    {attr: _get_proxy_method(attr) for attr in _INT_FALLBACK_METHODS},
)


class HugeInt(_IntFallback):
    """Store truly massive nubmers at full precision by saving them as gzipped strings in memory."""

    def __init__(self, new_value=0):
        int_new_value = int(new_value)
        self._hash = int_new_value.__hash__()
        self._is_huge = is_huge(int_new_value)

        if self._is_huge:
            self._value = compress(str(new_value).encode('utf-8', 'ascii'))
        else:
            self._value = int(new_value)

    def __str__(self):
        if self._is_huge:
            return decompress(self._value).decode()
        return str(self._value)

    def __repr__(self):
        if self._is_huge:
            full_str = decompress(self._value)
            return full_str[:16].decode() + '...({})'.format(len(full_str))
        return str(self._value)

    def __eq__(self, other):
        if other.__class__.__name__ == 'HugeInt':
            return self._value == other._value
        return self.to_int() == other

    def __hash__(self):
        return self._hash

    def to_int(self):
        if self._is_huge:
            return int(decompress(self._value))
        return self._value

    # TODO: properly implement all the it fallback methods directly on HugeInt
    def __getattr__(self, attr):
        return getattr(self.to_int(), attr)
