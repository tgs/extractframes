#!/usr/bin/env python
import subprocess
from nose.tools import *
from extract import parse_frame_range
import tempfile
import sys

def test_extract():
    assert_equal(0, subprocess.call(['./test_extract.sh']))


def test_parse_frame_range():
    assert_equal((100, 300), parse_frame_range('100-300'))




