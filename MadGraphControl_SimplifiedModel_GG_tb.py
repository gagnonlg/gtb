include ( 'MC15JobOptions/MadGraphControl_SimplifiedModelPreInclude.py' )

masses['1000021'] = float(runArgs.jobConfig[0].split("_")[4])
masses['1000005'] = float(runArgs.jobConfig[0].split("_")[5])
masses['1000006'] = float(runArgs.jobConfig[0].split("_")[5])
masses['1000022'] = float(runArgs.jobConfig[0].split("_")[6].split('.')[0]) 
masses['1000024'] = float(runArgs.jobConfig[0].split("_")[6].split('.')[0])+2
if masses['1000022']<0.5: masses['1000022']=0.5

gentype = str(runArgs.jobConfig[0].split("_")[2])
decaytype = str(runArgs.jobConfig[0].split("_")[3])

process = '''
generate p p > go go $ susysq susysq~ @1
add process p p > go go j $ susysq susysq~ @2
add process p p > go go j j $ susysq susysq~ @3
'''

njets = 2
evgenLog.info('Registered generation of Gtb grid '+str(runArgs.runNumber))

include ( 'MC15JobOptions/ParticleFilter.py' )
evgenLog.info('Gtt_filter is applied')
filtSeq += ParticleFilter("Gtt_filter")
filtSeq.Gtt_filter.PDG = 6 # top quark
filtSeq.Gtt_filter.MinParts = 4
filtSeq.Gtt_filter.Exclusive = True # require exactly 4 tops
filtSeq.Gtt_filter.StatusReq = -1 # ignore status
filtSeq.Gtt_filter.Ptcut = 0

evgenLog.info('top_filter is applied')
filtSeq += ParticleFilter("top_filter")
filtSeq.top_filter.PDG = 6 # top quark
filtSeq.top_filter.MinParts = 1
filtSeq.top_filter.Exclusive = False # require >= 1 top
filtSeq.top_filter.StatusReq = -1 # ignore status
filtSeq.top_filter.Ptcut = 0

#filtSeq.Expression = "(not Gtt_filter) and top_filter"

evgenConfig.contact  = ["louis.guillaume.gagnon@cern.ch"]
evgenConfig.keywords += ['simplifiedModel', 'gluino', 'neutralino', 'SUSY', 'stop', 'sbottom']
evgenConfig.description = 'gluino pair production and decay via off-shell stops and/or sbottoms, m_glu = %s GeV, m_stop/sbottom = %s GeV, m_N1 = %s GeV, m_C1 = % GeV'%(masses['1000021'],masses['1000005'],masses['1000022'],masses['1000024'])

genSeq.Pythia8.Commands += ["23:mMin = 0.2"]

include('MC15JobOptions/MadGraphControl_SimplifiedModelPostInclude.py')

if njets>0:
    genSeq.Pythia8.Commands += ["Merging:Process = pp>{go,1000021}{go,1000021}"]

