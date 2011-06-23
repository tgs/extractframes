#!/bin/bash


set -euv
make singlehtml

rm -rf build/gh-pages
git clone git@github.com:tgs/extractframes.git build/gh-pages

cd build/gh-pages
git checkout -t -b gh-pages origin/gh-pages

rm -r *
cp -r ../singlehtml/* .
git add -A
git commit -m "auto-update site"

set +v

echo "now run:"
echo
echo "cd `pwd`; git push origin gh-pages"
echo

