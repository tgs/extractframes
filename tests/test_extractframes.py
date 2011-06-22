#!/usr/bin/env python
from extractframes import *
from nose.tools import *
import tempfile
import unittest
import os
import shutil
import pdb
from extractframes.newmath import *

"""Test the extractframes module, which accomplishes the frame extraction."""

#
# Tests could go faster if many of them just tested the file copying part, and
# didn't bother with the video extraction part.  Once we know ffmpeg extracts
# 100 frames, that's enough.
#

class OneHundredFrameSetUp(object):
    def setup(self):
        self.in_file = 'fixtures/100frames.avi'
        self.out_dir = tempfile.mkdtemp()
        self.out_fmt = os.path.join(self.out_dir, 'img_%d.jpg')


    def teardown(self):
        shutil.rmtree(self.out_dir)

class TestBasicExtract(OneHundredFrameSetUp):
    def test_extract(self):
        extract(self.in_file, self.out_fmt)

        file_list = sorted(os.listdir(self.out_dir))
        assert_equal(len(file_list), 100)
        assert_equal(file_list[0], 'img_0.jpg')
        assert_true('img_99.jpg' in file_list)
        assert_true(32000 < os.path.getsize(os.path.join(self.out_dir, 'img_99.jpg')), 
                'Good quality not enabled?')


class TestHalfFrameRateExtract(OneHundredFrameSetUp):
    def test_half_frame_rate(self):
        extract(self.in_file, self.out_fmt, 
                ratio=0.5)

        file_list = sorted(os.listdir(self.out_dir))

        assert_equal(len(file_list), 50)


class TestLongWeirdRateExtract(OneHundredFrameSetUp):
    def test_long_weird_rates(self):
        self.setup() # call setup/teardown ourselves because of the yield...
        try:
            for ratio in float_range(0.1, 1.2, 0.1):
                yield do_extract_check, self.in_file, self.out_dir, ratio
                file_list = sorted(os.listdir(self.out_dir))
                for file_name in file_list:
                    os.remove(os.path.join(self.out_dir, file_name))
        finally:
            self.teardown()

def do_extract_check(in_file, out_dir, ratio):
    extract(in_file, os.path.join(out_dir, '%010d.jpg'), ratio=ratio)
    file_list = sorted(os.listdir(out_dir))

    assert_equal(len(file_list), math.floor(ratio * 100))


class TestExtractByRange(OneHundredFrameSetUp):
    def test_twenty(self):
        extract(self.in_file, self.out_fmt, in_frames=xrange(10, 30))
        file_list = sorted(os.listdir(self.out_dir))
        assert_equal(len(file_list), 20)

    @raises(ValueError)
    def test_range_past_end(self):
        # should raise exception because the last frame is #99
        extract(self.in_file, self.out_fmt, in_frames=xrange(0, 101))

    @raises(ValueError)
    def test_range_past_beginning(self):
        extract(self.in_file, self.out_fmt, in_frames=xrange(-1, 21))

class TestExtractByRangeToNum(OneHundredFrameSetUp):
    @raises(ValueError)
    def test_not_both_ratio_and_count(self):
        extract(self.in_file, self.out_fmt, ratio=2, out_count=30)


class TestExtractToNum(OneHundredFrameSetUp):
    def test_long_exact_ranges(self):
        self.setup()
        try:
            for num_out in range(0, 125, 6):
                yield do_extract_check_by_num, self.in_file, self.out_dir, num_out
                file_list = sorted(os.listdir(self.out_dir))
                for file_name in file_list:
                    os.remove(os.path.join(self.out_dir, file_name))
        finally:
            self.teardown()


class TestErrors():
    @raises(IOError)
    def test_no_out_dir(self):
        extract('doesnt_exist', '/path/to/nowhere')



def do_extract_check_by_num(in_file, out_dir, num_out):
    extract(in_file, os.path.join(out_dir, '%010d.jpg'), out_count=num_out)
    file_list = sorted(os.listdir(out_dir))

    assert_equal(len(file_list), num_out)
