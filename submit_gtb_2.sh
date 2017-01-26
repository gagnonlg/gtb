MASSES=$1

##########

cat <<EOF | qsub -d /lcg/storage15/atlas/gagnon/work -N gtb_$MASSES -joe -l nodes=1:ppn=5
. /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/user/atlasLocalSetup.sh
. $ATLAS_LOCAL_ROOT_BASE/packageSetups/localSetup.sh 'asetup AtlasProduction,19.2.5.15'

mkdir \${PBS_JOBID}_\${PBS_JOBNAME}
cd \${PBS_JOBID}_\${PBS_JOBNAME}

cp ~/dev/gtb/MadGraphControl_SimplifiedModel_GG_tb.py _MadGraphControl_SimplifiedModel_GG_tb.py

echo "include( 'MC15JobOptions/_MadGraphControl_SimplifiedModel_GG_tb.py' )" > \
     MC15.000000.MGPy8EG_A14N23LO_GG_tb_$MASSES.py

export ATHENA_PROC_NUMBER=5
Generate_tf.py --ecmEnergy=13000. \
	       --runNumber=000000 \
	       --firstEvent=1 \
	       --maxEvents=25000 \
	       --randomSeed=1207 \
	       --jobConfig=MC15.000000.MGPy8EG_A14N23LO_GG_tb_$MASSES.py \
	       --outputEVNTFile=gtb_${MASSES}_test.pool.root
EOF


