#!/usr/bin/env python
from nose.tools import *
from extractframes.framesource import *
import os

def test_frame_zero():
    fs = VideoFrameSource('fixtures/100frames.avi')
    res = fs.get_frame_file(0)
    assert_equal(os.path.basename(str(res)), '0000000001.jpg')

def test_frame_past_end():
    fs = VideoFrameSource('fixtures/100frames.avi')
    # last frame should be 99
    res = fs.get_frame_file(100)
    assert_equal(res, None)

@raises(IOError)
def test_nonexistant_source():
    fs = VideoFrameSource('/path/to/nowhere')
