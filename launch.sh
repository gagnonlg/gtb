. /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/user/atlasLocalSetup.sh
. $ATLAS_LOCAL_ROOT_BASE/packageSetups/localSetup.sh 'asetup AtlasProduction,19.2.5.5'


repo="/lcg/storage15/atlas/gagnon/work/2016-07-25_submit_gtb/gtb"

mkdir $JOBNAME
cd $JOBNAME

git clone $repo .

export ATHENA_PROC_NUMBER=$NJOBS
Generate_tf.py --ecmEnergy=13000. \
	       --runNumber=000000 \
	       --firstEvent=1 \
	       --maxEvents=100000 \
	       --randomSeed=9841 \
	       --jobConfig=MC15.000000.MGPy8EG_A14N23LO_GG_${NAME}_${MASSES}.py \
	       --outputEVNTFile=${NAME}_${MASSES}_test.pool.root


