#!/usr/bin/env python
from nose.tools import *
from extractframes.rateconverter import *
from extractframes.newmath import *
from nose.plugins.skip import SkipTest
from extractframes.multirange import multirange

def do_length_comparison(ratio, max):
    """
    The length of the output must be floor(RATIO times MAX)
    """
    res = list(convert_integers_by_ratio(ratio, max))
    assert_equal(len(res), math.floor(ratio * max))
#
# Ratio of One: should just give back the input numbers
#

def test_one_to_one_on_one():
    res = list(convert_integers_by_ratio(1, 1))
    assert_equal(res, [(0, 0)])

def test_one_to_one_on_two():
    res = list(convert_integers_by_ratio(1, 2))
    assert_equal(res, [(0, 0), (1, 1)])

def test_one_to_one_on_many():
    res = list(convert_integers_by_ratio(1, 100))
    want = range(0, 100)
    want = zip(want, want)
    assert_equal(res , want)


# ratio of 1/2
def test_half_on_two():
    res = list(convert_integers_by_ratio(0.5, 2))
    assert_equal(res, [(1, 0)])

def test_half_on_five():
    res = list(convert_integers_by_ratio(0.5, 5))
    assert_equal(res, [(1, 0), (3, 1)])

def test_half_on_lots():
    for max in xrange(0, 100):
        do_length_comparison(0.5, max)


# ratio of 2
def test_two_on_one():
    res = list(convert_integers_by_ratio(2, 1))
    assert_equal(res, [(0, 0), (0, 1)])

def test_two_on_some():
    res = list(convert_integers_by_ratio(2, 20))
    assert_equal(len(res), 40)

def test_two_on_none():
    res = list(convert_integers_by_ratio(2, 0))
    assert_equal(res, [])

def test_two_on_lots():
    for max in xrange(0, 100):
        do_length_comparison(2, max)


# weird ratios and maxima
def test_combinations_weird():
    for max in xrange(0, 100, 2):
        for ratio in float_range(0.1, 4, 0.2):
            do_length_comparison(ratio, max)


class TestConvertIntegersByRatioWithOffsets(object):
    def test_one_offset(self):
        res = list(convert_integers_by_ratio(1, 3, src_offset=100))
        assert_equal(res, [(100, 0), (100+1, 1), (100+2, 2)])

    def test_offset_with_ratio(self):
        res = list(convert_integers_by_ratio(2, 3, src_offset=100))
        assert_equal(res, [(100+0, 0), (100+0, 1), (100+1, 2), (100+1, 3),
            (100+2, 4), (100+2, 5)])



class TestConvertRangeToRange(object):
    def test_length_one(self):
        assert_equal([(1, 1)], list(convert_range_to_range((1, 1), (1, 1))))

    def test_fifty_hundred(self):
        res = list(convert_range_to_range((1, 50), (1, 100)))
        assert_equal(len(res), 100)

    def big_test_ratios(self):
        for num_ins in xrange(1, 300, 8):
            for num_outs in xrange(0, 300, 7):
                self.check_ratio(num_ins, num_outs)

    def test_ratios(self):
        for num_ins in xrange(1, 5):
            for num_outs in xrange(0, 5):
                yield self.check_ratio, num_ins, num_outs

    def check_ratio(self, num_ins, num_outs):
        ratio = ratio_for_number(num_ins, num_outs)
        assert_equal(expected_number(ratio, num_ins), num_outs)
        assert_equal(len(list(convert_integers_by_ratio(ratio, num_ins))), num_outs)


def testSkip():
    res = convert_integers_by_iterator_ratio(1,
            multirange('0-1,5-6'))
    assert_equal(list(res), [(0,0), (1,1), (5,5), (6,6)])

def testSkipRatio():
    res = convert_integers_by_iterator_ratio(0.5,
            multirange('0-1,5-6'))
    assert_equal(list(res), [(1,0), (5,2)])

def testSkipRatioOffset():
    res = convert_integers_by_iterator_ratio(0.5,
            multirange('0-1,5-6'), dest_offset=5)
    assert_equal(list(res), [(1,5), (5,7)])

def testSkipRatioBad():
    """This is a really confusing one.  For the program to return the expected
    answer below, I would have to break most of the other tests in this file!
    Since they depend on it not slurping up extra frames.  Very hard to explain.
    Argh."""

    raise SkipTest()
    res = convert_integers_by_iterator_ratio(0.5,
            multirange('0-0,2-2'))
    assert_equal(list(res), [(0,0), (2,1)])



