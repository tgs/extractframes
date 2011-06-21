#!/usr/bin/env python
from nose.tools import *
from extractframes.multirange import *

def testSingleRange():
    assert_equal([0,1,2,3,4], list(multirange('0-4')))

def testTwoRange():
    s = '0-2,10-12'
    assert_equal([0,1,2,10,11,12], list(multirange(s)))
    
def testThreeRange():
    s = '0-2,20-25,30-31'
    assert_equal([0,1,2,20,21,22,23,24,25,30,31], list(multirange(s)))

@raises(ValueError)
def testErrorOverlappingRanges():
    s = '0-10,5-15'
    list(multirange(s))


def testIsType():
    assert_equal(type(multirange), type)

#def testFloatParse():
    #s = '0.5-0.8'


