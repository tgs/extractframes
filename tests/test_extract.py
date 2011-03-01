#!/usr/bin/env python
import subprocess
from nose.tools import *
from extract import parse_range
import tempfile
import sys

def test_extract():
    assert_equal(0, subprocess.call(['./test_extract.sh']))


def test_parse_frame_range():
    assert_equal((100, 300), parse_range('100-300'))
    assert_equal((10.5, 37.7), parse_range('10.5-37.7'))




