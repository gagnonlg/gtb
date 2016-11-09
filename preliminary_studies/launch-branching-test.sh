. /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/user/atlasLocalSetup.sh
. $ATLAS_LOCAL_ROOT_BASE/packageSetups/localSetup.sh 'asetup AtlasProduction,19.2.5.5'

repo=/lcg/storage15/atlas/gagnon/work/2016-07-25_submit_gtb/gtb
name=ttbb
masses=1800_5000_100
path=${name}_${masses}_${F_TT}.test.pool.root


mkdir $JOBNAME
cd $JOBNAME

mkdir generation && cd generation
git clone $repo .


python2 change_branching.py $F_TT

Generate_tf.py --ecmEnergy=13000. \
	       --runNumber=000000 \
	       --firstEvent=1 \
	       --maxEvents=100000 \
	       --randomSeed=$RANDOM \
	       --jobConfig=MC15.000000.MGPy8EG_A14N23LO_GG_${name}_${masses}.py \
	       --outputEVNTFile=$path

cd ../
mkdir derivation && cd derivation
. $ATLAS_LOCAL_ROOT_BASE/packageSetups/localSetup.sh 'asetup 20.7.5.41,AtlasDerivation,gcc49,here'
Reco_tf.py --inputEVNTFile ../generation/$path --outputDAODFile $(basename $path) --reductionConf TRUTH3
