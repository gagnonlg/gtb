qsub -N generate_gtb \
     -d $PWD \
     -j oe \
     -l nodes=1:ppn=${NJOBS-20},nice=0 \
     launch.sh
