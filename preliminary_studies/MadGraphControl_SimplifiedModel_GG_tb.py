include ( 'MC15JobOptions/MadGraphControl_SimplifiedModelPreInclude.py' )


fields = runArgs.jobConfig[0].replace(".py","").split("_")
# 0                   1        2  3  4        5        6
# MC15.<dsid>.MGPy8EG_A14N23LO_GG_tb_<gluino>_<squark>_<neutralino>_<final state>.py

gentype = fields[2]
decaytype = fields[3]
gluino_mass = float(fields[4])
squark_mass = float(fields[5])
neutralino_mass = float(fields[6])
final_state = fields[7]

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

# Setup the filters
from GeneratorFilters.GeneratorFiltersConf import ParticleFilter

if final_state == '2top':
    # Keep only 2-top final states
    filtSeq += ParticleFilter("filter_2_top")
    filtSeq.filter_2_top.PDG = 6 # top quark
    filtSeq.filter_2_top.MinParts = 2
    filtSeq.filter_2_top.Exclusive = True # require exactly 2 tops
    filtSeq.filter_2_top.StatusReq = -1
    filtSeq.filter_2_top.Ptmin = 0
    filtSeq.Expression = "filter_2_top"

    # filter efficiency is 3/9, add small margin for other inefficiencies
    evt_multiplier = (9.0/3.0) * 1.5


elif final_state == '1-3top':
    # Keep only 1-top and 3-top final states
    filtSeq += ParticleFilter("filter_1_top")
    filtSeq.filter_1_top.PDG = 6 # top quark
    filtSeq.filter_1_top.MinParts = 1
    filtSeq.filter_1_top.Exclusive = True # require exactly 1 tops
    filtSeq.filter_1_top.StatusReq = -1
    filtSeq.filter_1_top.Ptmin = 0
    filtSeq += ParticleFilter("filter_3_top")
    filtSeq.filter_3_top.PDG = 6 # top quark
    filtSeq.filter_3_top.MinParts = 3
    filtSeq.filter_3_top.Exclusive = True # require exactly 3 tops
    filtSeq.filter_3_top.StatusReq = -1
    filtSeq.filter_3_top.Ptmin = 0
    filtSeq.Expression = "filter_1_top or filter_3_top"

    # filter efficiency is 4/9, add small margin for other inefficiencies
    evt_multiplier = (9.0/4.0) * 1.5


else:
   raise RuntimeError("invalid final state: {}".format(final_state))

evgenLog.info('final state: {}'.format(final_state))
evgenLog.info('filtSeq.Expression: {}'.format(filtSeq.Expression))
evgenLog.info('evt_multiplier: {}'.format(evt_multiplier))



include('MC15JobOptions/MadGraphControl_SimplifiedModelPostInclude.py')

