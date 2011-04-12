Overview
========

.. _overview:

What does it do?
----------------

The :program:`extract.py` script will take an input video and extract all the frames
from it as JPEG files.  It can give you just a particular range of the
frames, and it can change the frame rate by :ref:`Linear Frame Sampling`.  So
for instance, if you want half as many frames as there are in the input, it
will take every other frame.  If you want twice as many frames, it will take
every frame twice.  It can also select frames by time, not just frame number.

.. _correct-not-fast:

First make it correct, then make it fast
----------------------------------------

:program:`extract.py` places an emphasis on correctness rather than speed.  It uses
the `ffmpeg`_ program to extract all of the frames in the input video, at
the original frame rate.  Only then does it select particular frames to
copy, or change frame rates.  This is because :command:`ffmpeg` is not totally
reliable when you ask it to change rates.  It is used because of its very
extensive support for video formats.

.. _ffmpeg: http://www.ffmpeg.org/

When it extracts frames from video, :command:`ffmpeg` starts numbering
them from 1.  But for our purposes, it's more useful to have them
numbered from 0.  If this is a problem, it wouldn't be too hard to add
an option to change this.

Linear Frame Sampling
---------------------

:program:`extract.py` doesn't ever "make up" image data.  All it can do is
leave out or duplicate frames.  This might lead to problems with e.g. change
detection.  For example, take a video stream that has been converted from 25
to 30 frames per second:

.. only:: html or latex

        .. digraph:: conversion

           in0->out0
           in1->out1
           in2->out2
           in3->out3
           in4->out4
           in4->out5

.. only:: text

           in0->out0
           in1->out1
           in2->out2
           in3->out3
           in4->out4
           in4->out5
        

The changes between frame `out4` and frame `out5` will always be zero!  So
that means that, for example, :samp:`cam{N}_dyn_obj{M}` will have a spurious
zero, one time out of every 6 samples.

I'm not sure about the right way to deal with this.

