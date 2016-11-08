. /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/user/atlasLocalSetup.sh
. $ATLAS_LOCAL_ROOT_BASE/packageSetups/localSetup.sh 'asetup AtlasProduction,19.2.5.15'

mkdir ${PBS_JOBID}_${PBS_JOBNAME}
cd ${PBS_JOBID}_${PBS_JOBNAME}

git clone $REPO .

if [ "$NAME" = "2topC1" ]; then
    maxEvents=10000
elif [ "$NAME" = "2top" ]; then
    maxEvents=4000
else
    # 1top or 3top
    maxEvents=3000
fi

export ATHENA_PROC_NUMBER=$NJOBS
Generate_tf.py --ecmEnergy=13000. \
	       --runNumber=000000 \
	       --firstEvent=1 \
	       --maxEvents=$maxEvents \
	       --randomSeed=12507 \
	       --jobConfig=MC15.000000.MGPy8EG_A14N23LO_GG_tb_${MASSES}_${NAME}.py \
	       --outputEVNTFile=gtb_${NAME}_${MASSES}_test.pool.root


