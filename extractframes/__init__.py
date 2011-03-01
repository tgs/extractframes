#!/usr/bin/env python
import progressbar
import shutil
from framesource import VideoFrameSource
import tempfile
import decimal
import rateconverter 
import os

"""
extractframes package - extract frames from a video.

The top level module contains only one function, extract() which is the main
way you'd accomplish frame extractions.
"""

# maybe refactor this part so that the file movement is also testable
# separately from the extraction?

def extract(infile, outfile, ratio=None, in_bounds=None, quiet=True, out_count=None):
    if not os.path.isdir(os.path.dirname(outfile)):
        raise IOError('Destination directory %s does not exist!' % os.path.dirname(outfile))

    if ratio is not None and out_count is not None:
        raise ValueError('You can only specify one of ratio and out_count')
    elif ratio is None and out_count is None:
        ratio = 1

    frame_source = VideoFrameSource(infile, quiet=quiet)

    if not in_bounds:
        in_bounds = (0, frame_source.get_num_frames() - 1)

    if in_bounds[0] < 0 or in_bounds[1] > frame_source.get_num_frames() - 1:
        raise ValueError("Requested bounds %s don't fit in %d-frame video file"
                % (in_bounds, frame_source.get_num_frames()))

    in_count = in_bounds[1] - in_bounds[0] + 1

    if out_count is not None:
        ratio = rateconverter.ratio_for_number(in_count, out_count)

    iterator = rateconverter.convert_integers_by_ratio(ratio, in_count,
            src_offset=in_bounds[0])
    if not quiet:
        pbar = progressbar.ProgressBar(widgets=['Copying frames to destination',
            progressbar.Bar(), progressbar.ETA()])
        iterator = pbar(list(iterator))
    for src, dst in iterator:
        source = frame_source.get_frame_file(src)
        dest = outfile % dst

        shutil.copy(source, dest)






