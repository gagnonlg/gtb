#!/bin/bash

set -u
set -e

njobs=${NJOBS-10}

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

qsub -N gtb \
     -v "NJOBS=$njobs,MASSES=1900_5000_1,REPO=$SCRIPT_DIR" \
     -d $PWD \
     -j oe -k oe \
     -l nodes=1:ppn=$njobs,nice=0 \
     $PWD/launch_gtb.sh

