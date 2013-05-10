#!/bin/bash
set -eu

OUTDIR=`mktemp -d`

TMPDIR=`mktemp -d deleteme.XXXXXXXXX`

WHAT='Setting cleanup'
trap "{ ls $OUTDIR; echo FAIL \$WHAT; rm -rf $OUTDIR $TMPDIR; exit 255; }" ERR INT

WHAT='Making output dir'
test -d "$OUTDIR"

FMT='%05d.jpg'


function check_results() {
	FIRST_WHAT="$WHAT"
	trap "{ ls $OUTDIR; echo FAIL \$WHAT; rm -rf $OUTDIR; exit 255; }" ERR INT

	WHAT="$FIRST_WHAT: Output directory exists"
	test -d "$OUTDIR"

	FULL_FMT="$OUTDIR/$FMT"

	WHAT="$FIRST_WHAT: First frame doesn't exist"
	test -f `printf $FULL_FMT $1`

	WHAT="$FIRST_WHAT: Last frame doesn't exist"
	test -f `printf $FULL_FMT $2`

	NUM_FRAMES=$(($2 - $1 + 1))
	WHAT="$FIRST_WHAT: Number of frames isn't $NUM_FRAMES"
	test `ls $OUTDIR/*.jpg | wc -l` -eq $NUM_FRAMES

	WHAT="$FIRST_WHAT: Temp dir $TMPDIR isn't empty"
	test `ls $TMPDIR | wc -l` -eq 0

}

function clean_outdir() {
	trap "{ ls $OUTDIR; echo FAIL \$WHAT; rm -rf $OUTDIR; exit 255; }" ERR INT

	WHAT='Removing frames'
	rm "$OUTDIR"/*.jpg
}

WHAT='Running extract.py'
./extract.py fixtures/100frames.avi "$OUTDIR/$FMT"

check_results 0 99
clean_outdir


WHAT='Running extract.py --take'
./extract.py fixtures/100frames.avi "$OUTDIR/$FMT" --take 25-35

check_results 0 10
clean_outdir


WHAT='Trying to extract too many frames, should error'
./extract.py fixtures/100frames.avi "$OUTDIR/$FMT" --take 1-110 > /dev/null 2>&1 || true

WHAT="Number of frames is 0 after error"
test `ls $OUTDIR/ | wc -l` -eq 0

WHAT='Temp dir $TMPDIR is empty'
test `ls $TMPDIR | wc -l` -eq 0


WHAT='Invalid input file'
./extract.py /some/nonexistant.avi "$OUTDIR/$FMT" > /dev/null 2>&1 || true

WHAT="Number of frames is 0 after error"
test `ls $OUTDIR/ | wc -l` -eq 0

WHAT='Temp dir $TMPDIR is empty'
test `ls $TMPDIR | wc -l` -eq 0


WHAT='Cannot write to output'
./extract.py fixtures/100frames.avi /dir/that/doesnt/exist/$FMT > /dev/null 2>&1 || true

WHAT="Number of frames is 0 after error"
test `ls $OUTDIR/ | wc -l` -eq 0

WHAT='Temp dir $TMPDIR is empty'
test `ls $TMPDIR | wc -l` -eq 0


WHAT='Extract at 3/4 frame rate'
./extract.py fixtures/100frames.avi "$OUTDIR/$FMT" --take 0-99 --squish-to 75
check_results 0 74
clean_outdir


WHAT='Extract by time'
./extract.py fixtures/100frames.avi "$OUTDIR/$FMT" --take-times 0-1
check_results 0 29
clean_outdir

WHAT='Extract with fractional times'
./extract.py fixtures/100frames.avi "$OUTDIR/$FMT" --take-times 0.2-2.8
check_results 0 78
clean_outdir

WHAT='Extract with fractional times AND squish'
./extract.py fixtures/100frames.avi "$OUTDIR/$FMT" --take-times 0.2-2.8 --squish-to 15
check_results 0 14
clean_outdir

WHAT='Extract with keep-numbers'
./extract.py fixtures/100frames.avi "$OUTDIR/$FMT" --take 10-30 --keep-numbers
check_results 10 30
clean_outdir

WHAT='Extract with gaps'
./extract.py fixtures/100frames.avi "$OUTDIR/$FMT" --take 10-20,30-40
test `ls $OUTDIR/ | wc -l` -eq 22
for F in `seq 0 10; seq 20 30`; do
	test -f `printf "$OUTDIR/$FMT" $F`
done
clean_outdir

WHAT='Extract with keep-numbers AND stretch'
./extract.py fixtures/100frames.avi "$OUTDIR/$FMT" --take 10-30 --keep-numbers --stretch-to 41
check_results 10 50
clean_outdir

rm -rf $OUTDIR $TMPDIR





exit 0

