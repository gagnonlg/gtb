
def make_row(descr, dsid, jobopt, fs, af2):

    return ','.join([
        descr,
        str(dsid),
        '',
        jobopt,
        str(fs) if fs > 0 else '',
        str(af2) if af2 > 0 else '',
        '1',
        '','','','','','','','','','','','','',
        'MadGraph5 + Pythia8',
        '13000',
        '',
        '25ns spacing',
        '','','',''
    ])

def make_sample(dsid, gluino_mass, lsp_mass, final_state):
    descr = 'GG_tb_{}_5000_{}_{}'.format(gluino_mass, lsp_mass, final_state)

    if final_state in ['1top', '3top']:
        stats=3000
    elif final_state == '2topC1':
        stats=10000
    else: # final_state == '2top':
        stats=40000

    return make_row(
        descr=descr,
        dsid=dsid,
        jobopt='MC15.{}.MGPy8EG_A14N23LO_{}.py'.format(dsid, descr),
        fs=(stats if gluino_mass == 2300 and lsp_mass == 1 else 0),
        af2=stats
    )

def make_point(start_dsid, gluino_mass, lsp_mass):
    rows = []
    for i, state in enumerate(['1top', '2top', '2topC1', '3top']):
        rows.append(make_sample(start_dsid + i, gluino_mass, lsp_mass, state))
    return '\n'.join(rows)


header='Brief description,Data set ID,"ESD, RDO, DESD",JobOptions,Events (fullsim),Events (atlfast-II),Priority,Evgen,Simul,Merge,Digi,Reco,Rec merge,Rec tag,Atlfast,Atlfast merge,Atlfast tag,Cross-section,Filter eff,NLO xsec,Generator,Ecm,Release,Comment,Response,Trigger,Frozen shower,Filtered pile-up truth'

start_dsid = 373840

masses = [
    (1500, 1),
    (1900,1),
    (2100,1),
    (2300,1),
    (1900,600),
    (2100,600),
    (2300,600),
    (1800,1000),
    (2000,1000),
    (2100,1000),
    (1600,1000),
]

print header

for i, (mg, ml) in enumerate(masses):
    print make_point(start_dsid + i*4, mg, ml)
