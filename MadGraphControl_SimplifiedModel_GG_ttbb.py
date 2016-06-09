include ( 'MC15JobOptions/MadGraphControl_SimplifiedModelPreInclude.py' )


fields = runArgs.jobConfig[0].replace(".py","").split("_")
# 0                   1        2  3    4        5         6
# MC15.<dsid>.MGPy8EG_A14N23LO_GG_ttbb_<gluino>_<squark>_<neutralino>.py

gentype = fields[2]
decaytype = fields[3]
gluino_mass = float(fields[4])
squark_mass = float(fields[5])
neutralino_mass = float(fields[6])

masses['1000021'] = gluino_mass
masses['1000005'] = squark_mass # sbottom
masses['1000006'] = squark_mass # stop
masses['1000022'] = neutralino_mass

process = '''
generate p p > go go $ susysq susysq~ @1
add process p p > go go j $ susysq susysq~ @2
add process p p > go go j j $ susysq susysq~ @3
'''
njets = 2

evgenLog.info('GGttbb grid point {}'.format(runArgs.runNumber))
evgenLog.info('gluino mass: {}'.format(gluino_mass))
evgenLog.info('squark mass: {}'.format(squark_mass))
evgenLog.info('neutralino mass: {}'.format(neutralino_mass))

evgenConfig.contact  = ["louis.guillaume.gagnon@cern.ch"]
evgenConfig.keywords += ['simplifiedModel', 'gluino', 'neutralino', 'SUSY', 'boosted', 'top', 'bottom']
evgenConfig.description = 'gluino pair production and decay to tops and/or bottoms and LSP via off-shell stops and/or sbottoms'


if njets>0:
    genSeq.Pythia8.Commands += ["Merging:Process = pp>{go,1000021}{go,1000021}"]

# Filter-out pure Gtt and Gbb events
from GeneratorFilters.GeneratorFiltersConf import ParentTwoChildrenFilter

filtSeq += ParentTwoChildrenFilter('tt_bb_filter')
filtSeq.tt_bb_filter.PDGParent = [1000021] # gluino
filtSeq.tt_bb_filter.PDGChild = [5,6] # bottom, top

# filter efficiency is 50% + small margin for other inefficiencies
evt_multiplier = 2.2

include('MC15JobOptions/MadGraphControl_SimplifiedModelPostInclude.py')

