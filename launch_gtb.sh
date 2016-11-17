. /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/user/atlasLocalSetup.sh
. $ATLAS_LOCAL_ROOT_BASE/packageSetups/localSetup.sh 'asetup AtlasProduction,19.2.5.15'

mkdir ${PBS_JOBID}_${PBS_JOBNAME}
cd ${PBS_JOBID}_${PBS_JOBNAME}

git clone $REPO .

maxEvents=25000

export ATHENA_PROC_NUMBER=$NJOBS
Generate_tf.py --ecmEnergy=13000. \
	       --runNumber=000000 \
	       --firstEvent=1 \
	       --maxEvents=$maxEvents \
	       --randomSeed=12507 \
	       --jobConfig=MC15.000000.MGPy8EG_A14N23LO_GG_tb_${MASSES}.py \
	       --outputEVNTFile=gtb_${MASSES}_test.pool.root


