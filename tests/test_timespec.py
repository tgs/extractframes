#!/usr/bin/env python

from nose.tools import *
import extractframes.timespec as timespec

def test_runs():
    timespec.time_to_frame(0, rate=30)

def test_frame_starts_with_one():
    assert_equals(1, timespec.time_to_frame(0, rate=30))
    

def test_one_fps():
    assert_equals(2, timespec.time_to_frame(1, rate=1))


def test_30_fps():
    fnum = timespec.time_to_frame(0, rate=30)
    assert_equals(1, fnum)

    fnum = timespec.time_to_frame(1, rate=30)
    assert_equals(31, fnum)

def test_2997_fps():
    fnum = timespec.time_to_frame(0)
    assert_equals(1, fnum)

    # all the +1's are because of the damn indexing-from-1-or-0 thing.
    fnum = timespec.time_to_frame((1001 + 1) / 30.0)
    assert_equals(1001, fnum)

    fnum = timespec.time_to_frame(100101 / 30.0)
    assert_equals(100001, fnum)

    fnum = timespec.time_to_frame(10010001 / 30.0)
    assert_equals(10000001, fnum)


