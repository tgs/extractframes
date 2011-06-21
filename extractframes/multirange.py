#!/usr/bin/env python


def multirange(rangestr):
    """Take string like '1-10,12-40', and return the indicated integers"""
    parts = range_str.split('-')
    if len(parts) != 2:
        raise ValueError('Ranges must have exactly two parts, "start-end"')
    return xrange(parts[0], parts[1] + 1)


