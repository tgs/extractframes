#!/usr/bin/env python
import optparse
import extractframes
from extractframes.timespec import time_to_frame

parser = optparse.OptionParser(usage="%prog infile outfmt [options]")

parser.add_option('--take', dest="in_bounds", type="string",
        metavar="RANGE",
        help="Extract only frames in the given RANGE.  RANGE should look "
        "like 2345-9999, that is, two integers separated by a hyphen.  The "
        "first frame is frame 0.")
parser.add_option('--stretch-to', '--squish-to', dest='out_count', type='int',
        metavar='NUM', default=None,
        help="Linearly sample from input images to end up with NUM frames of output.  "
        "For instance, if your video is 50 frames long and you say --stretch-to 75, "
        "every other frame will be duplicated so that you get 1.5 * 50 = 75 frames.")
parser.add_option('--take-times', dest='in_times', type='string',
        metavar='TIMERANGE',
        help="Extract only frames that fall within the given time range, "
        "assuming that the frame rate of the video is 29.97 frames per second."
        "  TIMERANGE should look like 123.4-887, that is, two decimal numbers"
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
        raw_range = parse_range(opts.in_bounds)
        bounds_tuple = tuple(int(x) for x in raw_range)
        if any(t[0] != t[1] for t in zip(raw_range, bounds_tuple)):
            parser.error("Frame numbers must be integers")
    elif opts.in_times:
        bounds_tuple = tuple(time_to_frame(t) for t in parse_range(opts.in_times))
    else:
        bounds_tuple = None

    # set the first frame of output
    if opts.keep_numbers:
        out_offset = bounds_tuple[0]
    else:
        out_offset = 0


    if len(args) < 2:
        parser.error("Input file and Output file format are required")

    (src, dst) = args;
    extractframes.extract(src, dst, in_bounds=bounds_tuple, out_count=opts.out_count,
            quiet=False, out_offset=out_offset)

