import unittest

from gzint import HugeInt


class TestHugeInt(unittest.TestCase):

    def test_init(self):
        test_int = HugeInt()
        assert not test_int._is_huge
        assert test_int._value == 0
        assert test_int == 0
        assert str(test_int) == '0'
        assert repr(test_int) == '0'

    def test_comparisons(self):
        assert HugeInt(10) == HugeInt(10)
        assert HugeInt(10) == 10
        assert 10 == HugeInt(10)
        assert HugeInt(10**10000) == 10**10000
        assert HugeInt(10**1000000) == 10**1000000

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


if __name__ == '__main__':
    unittest.main()
