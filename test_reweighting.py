import sqlite3

import numpy as np
import ROOT

""" parameters """
XSEC = 1000.0 * 0.00276133
LUMI = 10.7
UNCERT = 0.3

""" database """
db = sqlite3.connect('gtb.sql')

""" background dict """
bkgnd_dict = {
    'gbb_A' : 1.2,
    'gbb_B' : 7.0,
    'gtt_0l_A' : 0.8,
    'gtt_0l_B' : 4.6,
    'gtt_1l_A' : 0.68,
    'gtt_1l_B' : 0.7,
    'gtt_1l_C' : 3.3,
}

""" sql WHERE clauses for signal regions """

gbb_common = '(nlepton == 0 AND dphimin4j > 0.4)'
gbb_A = ' AND '.join([
    gbb_common,
    'njet_70 >= 4',
    'nb >= 3',
    'met > 450',
    'meff4j > 1900',
])
gbb_B = ' AND '.join([
    gbb_common,
    'njet_30 >= 4',
    'nb >= 4',
    'met > 300',
    'meff4j > 1000'
])

gtt_0l_common = ' AND '.join([
    'njet_30 >= 8',
    'nb >= 3',
    'nlepton == 0',
    'dphimin4j > 0.4',
    'mtb > 80'
])
gtt_0l_A = ' AND '.join([
    gtt_0l_common,
    'met > 400',
    'meff > 2000',
    'mjsum > 200'
])
gtt_0l_B = ' AND '.join([
    gtt_0l_common,
    'met > 400',
    'meff > 1500',
    'mjsum > 150'
])

gtt_1l_common = '(nlepton >= 1 AND njet_30 >= 6)'
gtt_1l_A = ' AND '.join([
    gtt_1l_common,
    'nb >= 3',
    'mt > 200',
    'mtb > 120',
    'met > 200',
    'meff > 2000',
    'mjsum > 200'
])
gtt_1l_B = ' AND '.join([
    gtt_1l_common,
    'nb >= 3',
    'mt > 200',
    'mtb > 120',
    'met > 350',
    'meff > 1500',
    'mjsum > 150'
])
gtt_1l_C = ' AND '.join([
    gtt_1l_common,
    'nb >= 4',
    'mt > 150',
    'mtb > 80',
    'met > 200',
    'meff > 500'
])

""" calc yields """

def calc_yield(sr):
    d = np.zeros(5)
    for i in range(5):
        where = 'ntop = {} AND {}'.format(i,sr)
        tot, = db.execute('SELECT count(*) FROM dataset WHERE ntop = {}'.format(i))
        cnt, = db.execute('SELECT count(*) FROM dataset WHERE {}'.format(where))
        d[i] = XSEC * LUMI * float(cnt[0]) / float(tot[0])
        #print "=> SR:{} ntop:{} eff:{} nevt:{}".format(sr,i,float(cnt[0]) / float(tot[0]),d[i])
    return d

yield_dict = {
    'gbb_A' : calc_yield(gbb_A),
    'gbb_B' : calc_yield(gbb_B),
    'gtt_0l_A' : calc_yield(gtt_0l_A),
    'gtt_0l_B' : calc_yield(gtt_0l_B),
    'gtt_1l_A' : calc_yield(gtt_1l_A),
    'gtt_1l_B' : calc_yield(gtt_1l_B),
    'gtt_1l_C' : calc_yield(gtt_1l_C),
}

""" Make triangle plots """

def calc_branching(f_tt, f_bb):
    f_tb = 1 - f_tt - f_bb
    return np.array([
        f_bb * f_bb,
        f_bb * f_tb + f_tb * f_bb,
        f_bb * f_tt + f_tt * f_bb + f_tb * f_tb,
        f_tb * f_tt + f_tt * f_tb,
        f_tt * f_tt
    ])

def sr_yield(f_tt, f_bb, yields, include_1_3=True):
    br = calc_branching(f_tt, f_bb)
    if not include_1_3:
        br[1] = 0
        br[3] = 0
        br *= np.sum(br)
    assert(np.isclose(np.sum(br),1))
    return np.sum(br * yields)

def calc_triangle(yields, b):
    f_bb = np.linspace(0,1,100)
    f_tt = np.linspace(0,1,100)

    res = np.zeros((f_bb.shape[0],f_tt.shape[0]))
    for i in range(f_bb.shape[0]):
        for j in range(f_tt.shape[0]):
            if f_bb[i]+f_tt[j] > 1:
                res[i,j] = 0
            else:
                s = sr_yield(f_tt[i], f_bb[i], yields)
                # if f_bb[i] == 1:
                #     #print " -> (Gbb) s={}, b={}".format(s,b)
                res[i,j] = ROOT.RooStats.NumberCountingUtils.BinomialExpZ(s,b,UNCERT)

    return res

def calc_line(yields, b):
    """ ggttbb """
    f_bb = np.linspace(0, 1, 100)
    res = np.zeros_like(f_bb)
    for i, f in enumerate(f_bb):
        res[i] = sr_yield(f, 1 - f, yields, include_1_3=False)
    return res

def save_triangle(yields, b, sr_name):
    grid = calc_triangle(yields, b)
    np.savetxt('triangle_{}.gz'.format(sr_name), grid)

for sr in ['gbb_A', 'gbb_B', 'gtt_0l_A', 'gtt_0l_B', 'gtt_1l_A', 'gtt_1l_B', 'gtt_1l_C']:
    yields_signal = yield_dict[sr]
    #print "=> {}".format(sr)
    yield_bkgnd = bkgnd_dict[sr]

    triangle = calc_triangle(yields_signal, yield_bkgnd)
    line = calc_line(yields_signal, yield_bkgnd)

    np.savetxt('{}_triangle.gz'.format(sr), triangle)
    np.savetxt('{}_line.gz'.format(sr), line)

