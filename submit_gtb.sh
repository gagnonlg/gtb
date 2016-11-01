#!/bin/bash

set -u
set -e

name=$1
if [ ! $name = "2top" ] && [ ! $name = "1-3top" ]
then
    >&2 echo "process must be 2top or 1-3top"
fi

njobs=${NJOBS-10}

qsub -N $name \
     -v "NAME=$name,NJOBS=$njobs,MASSES=1900_5000_1" \
     -d /lcg/storage15/atlas/gagnon/work/ \
     -j oe -k oe \
     -l nodes=1:ppn=$njobs,nice=0 \
     $PWD/launch_gtb.sh
