#!/usr/bin/env python

from nose.tools import *
import extractframes.timespec as timespec

def test_runs():
    timespec.time_to_frame(0, rate=30)

def test_frame_starts_with_one():
    assert_equals(0, timespec.time_to_frame(0, rate=30))
    

def test_one_fps():
    assert_equals(1, timespec.time_to_frame(1, rate=1))


def test_30_fps():
    fnum = timespec.time_to_frame(0, rate=30)
    assert_equals(0, fnum)

    fnum = timespec.time_to_frame(1, rate=30)
    assert_equals(30, fnum)

def test_2997_fps():
    fnum = timespec.time_to_frame(0)
    assert_equals(0, fnum)

    fnum = timespec.time_to_frame((1001) / 30.0)
    assert_equals(1000, fnum)

    fnum = timespec.time_to_frame(100100 / 30.0)
    assert_equals(100000, fnum)

    fnum = timespec.time_to_frame(10010000 / 30.0)
    assert_equals(10000000, fnum)


