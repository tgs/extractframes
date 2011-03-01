#!/usr/bin/env python
import optparse
import extractframes

parser = optparse.OptionParser(usage="%prog infile outfmt [options]")

parser.add_option('--take', dest="in_bounds", type="string",
        metavar="RANGE",
        help="extract only frames in the given RANGE.  RANGE should look "
        "like 2345-9999, that is, two integers separated by a hyphen.  The "
        "first frame is frame 0.")
parser.add_option('--stretch-to', '--squish-to', dest='out_count', type='int',
        metavar='NUM', default=None,
        help="linearly sample from input images to end up with NUM frames of output.  "
        "For instance, if your video is 50 frames long and you say --stretch-to 75, "
        "every other frame will be duplicated so that you get 1.5 * 50 = 75 frames.")


def parse_frame_range(range_str):
    """Parses a frame range like 234-789 into a tuple (234, 789)
    """
    parts = range_str.split('-')
    return tuple(int(s) for s in parts)

if __name__ == '__main__':
    (opts, args) = parser.parse_args()
    if opts.in_bounds:
        bounds_tuple = parse_frame_range(opts.in_bounds)
    else:
        bounds_tuple = None
    if len(args) < 2:
        parser.error("Input file and Output file format are required")

    extractframes.extract(*args, in_bounds=bounds_tuple, out_count=opts.out_count,
            quiet=False)

