#!/usr/bin/env python
import math
import fractions

def convert_integers_by_ratio(ratio, num_inputs, src_offset=0, dest_offset=0):
    """Given an out:in ratio and a number of inputs, give the reassignments
    that will result in the correct number of output frames taken linearly from
    input frames.

    You can also specify a src_offset or dest_offset, which are added to the
    source or dest numbers.

    >>> list(convert_integers_by_ratio(0.5, 4))
    [(1, 0), (3, 1)]
    >>>
    """
    max_taken = -1
    for in_frame in xrange(0, num_inputs):
        out_frame = int(math.floor((in_frame + 1) * ratio)) - 1
        if out_frame > max_taken:
            for copy in xrange(max_taken + 1, out_frame + 1):
                yield (in_frame + src_offset, copy + dest_offset)
            max_taken = out_frame

def expected_number(ratio, num_inputs):
    return math.floor(ratio * num_inputs)

def ratio_for_number(num_inputs, num_outputs):
    return fractions.Fraction(num_outputs, num_inputs)

def frames_in_range(bounds):
    return bounds[1] + 1 - bounds[0]

def convert_range_to_range(in_bounds, out_bounds):
    num_outs = frames_in_range(out_bounds)
    num_ins = frames_in_range(in_bounds)
    ratio = ratio_for_number(num_ins, num_outs)
    return convert_integers_by_ratio(ratio, num_ins,
            src_offset=in_bounds[0],
            dest_offset=out_bounds[0])

