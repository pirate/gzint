import unittest

try:
    from .main import HugeInt
except SystemError:
    print('''Tests must be run using:
    python -m gzint.tests
    or
    python setup.py test''')
    raise SystemExit(1)


class TestHugeInt(unittest.TestCase):

    # share one copy of these between all tests for speed reasons
    large_int = 10**1000000
    large = HugeInt(large_int)

    def test_init(self):
        zero = HugeInt()
        assert not zero._is_huge
        assert zero._value == 0
        assert str(zero) == '0'
        assert repr(zero) == '0'

        assert self.large._is_huge
        assert str(self.large) == str(self.large_int)
        assert repr(self.large) == '1000000000000000...(1000001)'

    def test_comparisons(self):
        assert HugeInt(0) == 0
        assert HugeInt(10) == 10
        assert HugeInt(10) == HugeInt(10)
        assert 10 == HugeInt(10)

        assert self.large == self.large
        assert self.large == self.large_int

    def test_identity(self):
        huge_ints = {HugeInt(5), HugeInt(6), 7}
        assert 5 in huge_ints
        assert HugeInt(6) in huge_ints
        assert HugeInt(7) in huge_ints

    def test_math(self):
        assert type(HugeInt(10) + 10) is HugeInt
        assert HugeInt(10) + 10 == 20
        assert HugeInt(20) - 20 == 0
        assert HugeInt(10) + HugeInt(10) == 20
        assert HugeInt(10) + HugeInt(10) == HugeInt(20)
        assert HugeInt(20) / HugeInt(10) == 2
        assert self.large + 1 == self.large_int + 1


if __name__ == '__main__':
    unittest.main()
