#!/usr/bin/env python
import optparse
import extractframes
from extractframes.timespec import time_to_frame
from extractframes.multirange import multirange

parser = optparse.OptionParser(usage="""%prog infile outfmt [options]

For more documentation, see http://tgs.github.com/extractframes/""")

parser.add_option('--take', dest="in_bounds", type="string",
        metavar="RANGES",
        help="Extract only frames in the given RANGE.  RANGES should look "
        "like '1-10,500-777,2345-9999', that is, comma-separated groups of two "
        "integers separated by a hyphen.  The first frame is frame 0.")
parser.add_option('--stretch-to', '--squish-to', dest='out_count', type='int',
        metavar='NUM', default=None,
        help="Linearly sample from input images to end up with NUM frames of output.  "
        "For instance, if your video is 50 frames long and you say --stretch-to 75, "
        "every other frame will be duplicated so that you get 1.5 * 50 = 75 frames.")
parser.add_option('--take-times', dest='in_times', type='string',
        metavar='TIMERANGES',
        help="Extract only frames that fall within the given time range, "
        "assuming that the frame rate of the video is 29.97 frames per second."
        "  TIMERANGES should look like '123.4-887,900-1000.4', that is, "
        "comma-separated groups of two decimal numbers"
        " separated by a hyphen, specifying the number of seconds from"
        " the start of the video.")
parser.add_option('--keep-numbers', dest='keep_numbers', action='store_true',
        default=False,
        help="Instead of renumbering the extracted frames to start at 0, "
        "number them starting with the first frame number that was extracted.  "
        "So if you say '--take 5-10 --keep-numbers', the output frames will "
        "be numbered from 5 to 10.")


def parse_range(range_str):
    """Parses a range like 234-789 into a tuple (234, 789)
    """
    parts = range_str.split('-')
    if len(parts) != 2:
        parser.error("Ranges can only have two parts: start-end")
    return tuple(float(s) for s in parts)

if __name__ == '__main__':
    (opts, args) = parser.parse_args()

    if opts.in_bounds and opts.in_times:
        parser.error("Options --take and --take-times are mutually exclusive")
    elif opts.in_bounds:
        frames = multirange(opts.in_bounds)
    elif opts.in_times:
        parse = lambda x: time_to_frame(float(x))
        frames = multirange(opts.in_times, parser=parse)
    else:
        frames = None

    # set the first frame of output
    if opts.keep_numbers:
        out_offset = frames[0]
    else:
        out_offset = 0


    if len(args) < 2:
        parser.error("Input file and Output file format are required")

    (src, dst) = args;
    extractframes.extract(src, dst, in_frames=frames, out_count=opts.out_count,
            quiet=False, out_offset=out_offset)


