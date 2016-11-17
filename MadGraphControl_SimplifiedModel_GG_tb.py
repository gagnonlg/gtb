include ( 'MC15JobOptions/MadGraphControl_SimplifiedModelPreInclude.py' )


fields = runArgs.jobConfig[0].replace(".py","").split("_")
# 0                   1        2  3  4        5        6
# MC15.<dsid>.MGPy8EG_A14N23LO_GG_tb_<gluino>_<squark>_<neutralino>.py

gentype = fields[2]
decaytype = fields[3]
gluino_mass = float(fields[4])
squark_mass = float(fields[5])
neutralino_mass = float(fields[6])

masses['1000021'] = gluino_mass
masses['1000005'] = squark_mass # sbottom
masses['1000006'] = squark_mass # stop
masses['1000022'] = neutralino_mass
masses['1000024'] = neutralino_mass + 2 # chargino_1

process = '''
generate p p > go go $ susysq susysq~ @1
add process p p > go go j $ susysq susysq~ @2
add process p p > go go j j $ susysq susysq~ @3
'''
njets = 2

evgenLog.info('Gtb grid point {}'.format(runArgs.runNumber))
evgenLog.info('gluino mass: {}'.format(gluino_mass))
evgenLog.info('squark mass: {}'.format(squark_mass))
evgenLog.info('neutralino mass: {}'.format(neutralino_mass))

evgenConfig.contact  = ["louis.guillaume.gagnon@cern.ch"]
evgenConfig.keywords += ['simplifiedModel', 'gluino', 'neutralino', 'SUSY', 'boosted', 'top', 'bottom']
evgenConfig.description = 'gluino pair production and decay to tops and bottoms + LSP via off-shell stops and/or sbottoms'


if njets>0:
    genSeq.Pythia8.Commands += ["Merging:Process = pp>{go,1000021}{go,1000021}"]

# Setup the filters to veto Gtt and Gbb events
from GeneratorFilters.GeneratorFiltersConf import ParticleFilter

# recognize Gtt events
filtSeq += ParticleFilter("Gtt_filter")
filtSeq.Gtt_filter.PDG = 6 # top quark
filtSeq.Gtt_filter.MinParts = 4
filtSeq.Gtt_filter.Exclusive = True # require exactly 4 tops
filtSeq.Gtt_filter.StatusReq = -1 # ignore status
filtSeq.Gtt_filter.Ptcut = 0

filtSeq += ParticleFilter("top_filter")
filtSeq.top_filter.PDG = 6 # top quark
filtSeq.top_filter.MinParts = 1
filtSeq.top_filter.Exclusive = False # require >= 1 top
filtSeq.top_filter.StatusReq = -1 # ignore status
filtSeq.top_filter.Ptcut = 0

filtSeq.Expression = "(not Gtt_filter) and top_filter"

# filter efficiency is 7/9
# add small margin for inefficiencies
evt_multiplier = 9.0/7.0 * 1.5

evgenLog.info('filtSeq.Expression: {}'.format(filtSeq.Expression))
evgenLog.info('evt_multiplier: {}'.format(evt_multiplier))



include('MC15JobOptions/MadGraphControl_SimplifiedModelPostInclude.py')

