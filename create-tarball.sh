#!/bin/sh
set -C -e

set -x
rm -Rf javamail~mercurial/
hg clone http://kenai.com/hg/javamail~mercurial
( cd ./javamail~mercurial && hg archive -r JAVAMAIL-1_4_6 -X doc/ ../javamail-1.4.6 )
rm -Rf javamail~mercurial/

tar cvf javamail-1.4.6-clean.tar.gz javamail-1.4.6/

