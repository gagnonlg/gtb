. /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/user/atlasLocalSetup.sh
. $ATLAS_LOCAL_ROOT_BASE/packageSetups/localSetup.sh 'asetup AtlasProduction,19.2.5.5'


datadir=/lcg/storage15/atlas/gagnon/work/generate_gtb

wdir=run_$(date --iso=seconds)
mkdir $wdir
cd $wdir

cp $datadir/MC15.000000.MGPy8EG_A14N23LO_GG_tbn1_1800_5000_100.py .
cp $datadir/MadGraphControl_SimplifiedModel_GG_tbn1.py .
cp $datadir/param_card.SM.GG.tbn1.dat .

export ATHENA_PROC_NUMBER=$NJOBS
Generate_tf.py --ecmEnergy=13000. \
	       --runNumber=000000 \
	       --firstEvent=1 \
	       --maxEvents=-1 \
	       --randomSeed=8461 \
	       --jobConfig=MC15.000000.MGPy8EG_A14N23LO_GG_tbn1_1800_5000_100.py \
	       --outputEVNTFile=gtb_test.pool.root


