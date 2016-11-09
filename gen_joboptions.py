
def make_filename(dsid, gluino_mass, lsp_mass, final_state):
    descr = 'GG_tb_{}_5000_{}_{}'.format(gluino_mass, lsp_mass, final_state)
    return 'MC15.{}.MGPy8EG_A14N23LO_{}.py'.format(dsid, descr)

def make_jobopts(start_dsid, gluino_mass, lsp_mass):

    for i, state in enumerate(['1top', '2top', '2topC1', '3top']):
        path = make_filename(start_dsid + i*4, gluino_mass, lsp_mass, state)
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
    (1800,1000),
    (2000,1000),
    (2100,1000),
    (1600,1000),
]

for i, (mg, ml) in enumerate(masses):
    make_jobopts(start_dsid + i*4, mg, ml)
