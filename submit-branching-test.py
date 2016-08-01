import os
import subprocess
import time

import numpy as np

def call(args):
    return subprocess.check_output(['/usr/bin/env'] + args)

def submit(f_tt):
    date = call(['date', '--iso=seconds']).replace('\n','')
    jobname = 'branching-test-{}-{}'.format(f_tt, date)
    print '=> {}'.format(jobname)
    call([
        qsub,
        '-N', jobname,
        '-d', os.getcwd(),
        '-joe',
        '-l', 'nice=0',
        '-v', 'JOBNAME={},F_TT={}'.format(jobname, f_tt),
        'launch-branching-test.sh'
    ])
    time.sleep(0.5)

for f_tt in np.linspace(0,1,5):
    submit(f_tt)

