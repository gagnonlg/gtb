
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

def make_point(dsid, gluino_mass, lsp_mass):
    descr = 'GG_tb_{}_5000_{}'.format(gluino_mass, lsp_mass)

    stats = 25000

    return make_row(
        descr=descr,
        dsid=dsid,
        jobopt='MC15.{}.MGPy8EG_A14N23LO_{}.py'.format(dsid, descr),
        fs=(stats if gluino_mass == 2300 and lsp_mass == 1 else 0),
        af2=stats
    )

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
    (1600,1000),
    (1800,1000),
    (2000,1000),
    (2100,1000),
]

print header

for i, (mg, ml) in enumerate(masses):
    print make_point(start_dsid + i, mg, ml)
