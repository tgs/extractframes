#!/bin/bash
set -eu

if [ ! -f './numcp.py' ]; then
	echo "Run this script from the root of the source distribution"
	exit 1
fi

OUTDIR=`mktemp -d`

TMPDIR=`mktemp -d deleteme.XXXXXXXXX`

WHAT='Setting cleanup'
trap "{ ls $OUTDIR; echo FAIL \$WHAT; rm -rf $OUTDIR $TMPDIR; exit 255; }" ERR INT

WHAT='Making output dir'
test -d "$OUTDIR"

WHAT='Populating input dir'
for NUM in `seq 0 150`; do
	echo $NUM > "$TMPDIR/$NUM.txt"
done


WHAT='Running numcp'
./numcp.py -s -a 35 "$TMPDIR"/*.txt "$OUTDIR" > /dev/null

WHAT='Determining files are in correct place'
for FILE in "$OUTDIR"/*.txt; do
	BASENAME="`basename $FILE`"
	FNUM="${BASENAME/.txt}"

	IDENT=`cat "$FILE"`

	test $FNUM -eq $(($IDENT + 35))
done

rm -rf $OUTDIR $TMPDIR





exit 0

