. /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/user/atlasLocalSetup.sh
. $ATLAS_LOCAL_ROOT_BASE/packageSetups/localSetup.sh 'asetup AtlasProduction,19.2.5.5'


repo=/home/zp/gagnon/dev/gtb

mkdir $JOBNAME
cd $JOBNAME

git clone $repo .

export ATHENA_PROC_NUMBER=$NJOBS
Generate_tf.py --ecmEnergy=13000. \
	       --runNumber=000000 \
	       --firstEvent=1 \
	       --maxEvents=10000 \
	       --randomSeed=750 \
	       --jobConfig=MC15.000000.MGPy8EG_A14N23LO_GG_${NAME}_1800_5000_100.py \
	       --outputEVNTFile=${NAME}_test.pool.root


