set -u
set -e
path=$(readlink -f $1)
jobdep=$2
jobname=derivation_$(basename $path .pool.root)_$(date --iso=seconds)

echo "dependency: $jobdep"
cat <<EOF | qsub -N $jobname -d /lcg/storage15/atlas/gagnon/work -joe -l nice=0 -W depend=afterok:$jobdep
mkdir $jobname
cd $jobname
. /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/user/atlasLocalSetup.sh
. $ATLAS_LOCAL_ROOT_BASE/packageSetups/localSetup.sh 'asetup 20.7.5.41,AtlasDerivation,gcc49,here'
Reco_tf.py --inputEVNTFile $path --outputDAODFile $(basename $path | sed 's/.pool.root/TRUTH3.root/') --reductionConf TRUTH3
EOF
