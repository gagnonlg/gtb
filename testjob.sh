set -u
set -e

cat <<EOF | qsub -d $PWD -N gtb-testjob-1 -j oe -l nice=0
rm -f testjob-1
mkdir -p testjob-1
cd testjob-1
. /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/user/atlasLocalSetup.sh
. $ATLAS_LOCAL_ROOT_BASE/packageSetups/localSetup.sh 'asetup 20.7.5.41,AtlasDerivation,gcc49,here'
Generate_tf.py --ecmEnergy=13000. --runNumber=373840 --firstEvent=1 --maxEvents=-1 --randomSeed=123 --jobConfig=/cvmfs/atlas.cern.ch/repo/sw/Generators/MC15JobOptions/latest/share/DSID373xxx/MC15.373840.MGPy8EG_A14N23LO_GG_tb_1500_5000_1.py  --outputEVNTFile=testjob.pool.root
EOF


sleep 0.5s

cat <<EOF | qsub -d $PWD -N gtb-testjob-2 -j oe -l nice=0
rm -f testjob-2
mkdir -p testjob-2
cd testjob-2
. /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/user/atlasLocalSetup.sh
. $ATLAS_LOCAL_ROOT_BASE/packageSetups/localSetup.sh 'asetup 20.7.5.41,AtlasDerivation,gcc49,here'
Generate_tf.py --ecmEnergy=13000. --runNumber=373845 --firstEvent=1 --maxEvents=-1 --randomSeed=123 --jobConfig=/cvmfs/atlas.cern.ch/repo/sw/Generators/MC15JobOptions/latest/share/DSID373xxx/MC15.373845.MGPy8EG_A14N23LO_GG_tb_2100_5000_600.py --outputEVNTFile=testjob.pool.root
EOF


sleep 0.5s

cat <<EOF | qsub -d $PWD -N gtb-testjob-3 -j oe -l nice=0
rm -f testjob-3
mkdir -p testjob-3
cd testjob-3
. /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/user/atlasLocalSetup.sh
. $ATLAS_LOCAL_ROOT_BASE/packageSetups/localSetup.sh 'asetup 20.7.5.41,AtlasDerivation,gcc49,here'
Generate_tf.py --ecmEnergy=13000. --runNumber=373850 --firstEvent=1 --maxEvents=-1 --randomSeed=123 --jobConfig=/cvmfs/atlas.cern.ch/repo/sw/Generators/MC15JobOptions/latest/share/DSID373xxx/MC15.373850.MGPy8EG_A14N23LO_GG_tb_2100_5000_1000.py --outputEVNTFile=testjob.pool.root
EOF

