#!/bin/bash

set -u
set -e

name=$1
if [ ! $name = "2top" ] && [ ! $name = "2topC1" ] && [ ! $name = "1top" ] && [ ! $name = "3top" ]
then
    >&2 echo "process must be 2top or 2topC1 or 1top or 3top"
fi

njobs=${NJOBS-10}

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

qsub -N $name \
     -v "NAME=$name,NJOBS=$njobs,MASSES=1900_5000_1,REPO=$SCRIPT_DIR" \
     -d /lcg/storage15/atlas/gagnon/work/2016-11-07_gtb/ \
     -j oe -k oe \
     -l nodes=1:ppn=$njobs,nice=0 \
     $PWD/launch_gtb.sh

