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

if final_state in ['2top', '2topC1']:
    # Keep only 2-top final states
    
    filtSeq += ParticleFilter("filter_2_top")
    filtSeq.filter_2_top.PDG = 6 # top quark
    filtSeq.filter_2_top.MinParts = 2
    filtSeq.filter_2_top.Exclusive = True # require exactly 2 tops
    filtSeq.filter_2_top.StatusReq = -1
    filtSeq.filter_2_top.Ptcut = 0

    filtSeq += ParticleFilter("filter_chargino")
    filtSeq.filter_chargino.PDG = 1000024
    filtSeq.filter_chargino.MinParts = 2
    filtSeq.filter_chargino.Exclusive = True # exactly 2 charginos
    filtSeq.filter_chargino.StatusReq = -1
    filtSeq.filter_chargino.Ptcut = 0

    if final_state == '2top':
        # keep only events where tops from same gluino
        # this means there are no charginos in the final stat
        filtSeq.Expression = "filter_2_top and (not filter_chargino)"

        # filter efficiency is 2/9
        evt_multiplier = 9.0/2.0

    else:
        # final_state == '2topC1'
        # keep only events where tops from different gluinos
        # this means there are exactly 2 charginos in final state
        filtSeq.Expression = "filter_2_top and filter_chargino"

        # filter efficiency is 1/9
        evt_multiplier = 9.0



elif final_state == '1-3top':
    # Keep only 1-top and 3-top final states
    filtSeq += ParticleFilter("filter_1_top")
    filtSeq.filter_1_top.PDG = 6 # top quark
    filtSeq.filter_1_top.MinParts = 1
    filtSeq.filter_1_top.Exclusive = True # require exactly 1 tops
    filtSeq.filter_1_top.StatusReq = -1
    filtSeq.filter_1_top.Ptcut = 0
    filtSeq += ParticleFilter("filter_3_top")
    filtSeq.filter_3_top.PDG = 6 # top quark
    filtSeq.filter_3_top.MinParts = 3
    filtSeq.filter_3_top.Exclusive = True # require exactly 3 tops
    filtSeq.filter_3_top.StatusReq = -1
    filtSeq.filter_3_top.Ptcut = 0
    filtSeq.Expression = "filter_1_top or filter_3_top"

    # filter efficiency is 4/9
    evt_multiplier = 9.0/4.0


else:
   raise RuntimeError("invalid final state: {}".format(final_state))

# add small margin for inefficiencies
evt_multiplier *= 1.5

evgenLog.info('final state: {}'.format(final_state))
evgenLog.info('filtSeq.Expression: {}'.format(filtSeq.Expression))
evgenLog.info('evt_multiplier: {}'.format(evt_multiplier))



include('MC15JobOptions/MadGraphControl_SimplifiedModelPostInclude.py')

