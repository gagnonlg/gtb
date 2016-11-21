def make_filename(dsid, gluino_mass, lsp_mass):
    descr = 'GG_tb_{}_5000_{}'.format(gluino_mass, lsp_mass)
    return 'MC15.{}.MGPy8EG_A14N23LO_{}.py'.format(dsid, descr)

def make_jobopts(dsid, gluino_mass, lsp_mass):

    path = make_filename(dsid, gluino_mass, lsp_mass)
    with open(path, 'w') as jobopt:
        jobopt.write("include( 'MC15JobOptions/MadGraphControl_SimplifiedModel_GG_tb.py' )\n")


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

for i, (mg, ml) in enumerate(masses):
    make_jobopts(start_dsid + i, mg, ml)
