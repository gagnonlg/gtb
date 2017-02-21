#!/bin/bash

set -u
set -e

masses=1800_5000_200

njobs=${NJOBS-10}

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

jobid=$(qsub -N gtb \
	     -v "NJOBS=$njobs,MASSES=$masses,REPO=$SCRIPT_DIR" \
	     -d /lcg/storage15/atlas/gagnon/work/ \
	     -j oe -k oe \
	     -l nodes=1:ppn=$njobs,nice=0 \
	     $PWD/launch_gtb.sh)

sleep 0.5s

jobdep=$(echo $jobid | awk -F. '{print $1}')
path=/lcg/storage15/atlas/gagnon/work/${jobid}_gtb/gtb_${masses}_test.pool.root
jobname=derivation_$(basename $path .pool.root)_$(date --iso=seconds)

cat <<EOF | qsub -N gtb-derivation -d /lcg/storage15/atlas/gagnon/work -joe -l nice=0 -W depend=afterok:$jobdep
mkdir $jobname
cd $jobname
. /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/user/atlasLocalSetup.sh
. $ATLAS_LOCAL_ROOT_BASE/packageSetups/localSetup.sh 'asetup 20.7.5.41,AtlasDerivation,gcc49,here'
Reco_tf.py --inputEVNTFile $path --outputDAODFile $(basename $path | sed 's/.pool.root/TRUTH3.root/') --reductionConf TRUTH3
EOF
