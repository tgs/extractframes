#!/usr/bin/env python
# numcp - copy files to sequentially numbered files

from optparse import OptionParser
import re
from os.path import *
from shutil import copy2
import operator

usage = """usage: %prog [options] src [src src src...] DESTDIR
%prog: Copy source files to sequentially numbered files in DESTDIR

Examples:

%prog foo/a foo/b bar/c quux
    Copies the three files foo/a.txt, foo/b.zip, and bar/c to the 
    directory quux, as files 0000.txt, 0001.zip, and 0002, respectively.

%prog -a 10 foo/* quux
    Copies the files in foo/ to quux, starting the numbering with 10
    rather than 0."""

parser = OptionParser(usage=usage)

parser.add_option("-f", "--format", dest="format", default=None,
    help="""The format for the name of the destination files.  For example,
"%04d.jpg".  The default is to copy each file to a 4-digit number, zero-padded,
with the same extension as the original file.""")
parser.add_option("-a", "--add", dest="offset", type="int", default=0,
    help="OFFSET is added to each destination's number")
parser.add_option("-s", "--sort", action="store_true", default=False,
    dest="sort",
    help="Do a numerical sort on the input files before assigning them numbers")

(opts, args) = parser.parse_args()

if len(args) < 2:
    parser.print_help()
    exit(1)



destdir = args[-1]
srcfiles = args[0:-1]




def name_to_number(file_name):
    """Extracts the last number found in a string.

    For instance, name_to_number("img_234.jpg") would return 234."""
    numbers = re.findall(r"(\d+)", file_name)
    if numbers:
        return int(numbers[-1])
    else:
        return None



if opts.sort:
    srcfiles.sort(key=name_to_number)

for (index, src) in enumerate(srcfiles):
    index = index + opts.offset
    if opts.format:
        dest = join(destdir, opts.format % index)
    else:
        if '.' in src:
            ext = '.' + src.rsplit('.', 1)[1]
        else:
            ext = ''
        dest = join(destdir, ('%04d' % index) + ext)
    print src, "->", dest
    copy2(src, dest)


