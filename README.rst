extractframes
====

This is a program that uses `ffmpeg`_ to extract JPG frames from a
video, and then uses a simple and well-tested algorithm to linearly
change the frame rate, if requested, and take only a certain range of
the frames.

I had to write this script because, when `ffmpeg` does
frame-rate changes, it's not accurate down to the frame level.  For
instance, if you extract and tell it to use 1/2 the frame rate, it
doesn't give you exactly half of the frames.  `extract.py`, on
the other hand, will give you exactly every other frame.



For more details and usage examples and stuff, see `the documentation`_.




.. _ffmpeg: http://www.ffmpeg.org/
.. _the documentation: http://tgs.github.com/extractframes/

