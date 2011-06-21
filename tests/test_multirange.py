#!/usr/bin/env python
from nose.tools import *
from extractframes.multirange import *

def testSingleRange():
    assert_equal([0,1,2,3,4], list(multirange('0-4')))
    

