import logging

import numpy as np

LOGGER = logging.getLogger('signal_regions')

luminosity_for_background = 10.7
signal_regions = {}

gbb_common = '(nlepton == 0 AND dphimin4j > 0.4)'
signal_regions['gbb_A'] = ' AND '.join([
    gbb_common,
    'njet_70 >= 4',
    'nb >= 3',
    'met > 450',
    'meff4j > 1900',
])

signal_regions['gbb_B'] = ' AND '.join([
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

signal_regions['gtt_0l_A'] = ' AND '.join([
    gtt_0l_common,
    'met > 400',
    'meff > 2000',
    'mjsum > 200'
])

signal_regions['gtt_0l_B'] = ' AND '.join([
    gtt_0l_common,
    'met > 400',
    'meff > 1500',
    'mjsum > 150'
])

gtt_1l_common = '(nlepton >= 1 AND njet_30 >= 6)'
signal_regions['gtt_1l_A'] = ' AND '.join([
    gtt_1l_common,
    'nb >= 3',
    'mt > 200',
    'mtb > 120',
    'met > 200',
    'meff > 2000',
    'mjsum > 200'
])
signal_regions['gtt_1l_B'] = ' AND '.join([
    gtt_1l_common,
    'nb >= 3',
    'mt > 200',
    'mtb > 120',
    'met > 350',
    'meff > 1500',
    'mjsum > 150'
])
signal_regions['gtt_1l_C'] = ' AND '.join([
    gtt_1l_common,
    'nb >= 4',
    'mt > 150',
    'mtb > 80',
    'met > 200',
    'meff > 500'
])

backgrounds = {
    'gbb_A' : 1.2,
    'gbb_B' : 7.0,
    'gtt_0l_A' : 0.8,
    'gtt_0l_B' : 4.6,
    'gtt_1l_A' : 0.68,
    'gtt_1l_B' : 0.7,
    'gtt_1l_C' : 3.3,
}

names = [
    'gbb_A',
    'gbb_B',
    'gtt_0l_A',
    'gtt_0l_B',
    'gtt_1l_A',
    'gtt_1l_B',
    'gtt_1l_C',
]

def get_yields_dict(db, xsec):
    yield_dict = {}
    for name in names:
        LOGGER.debug('calculating yields for region %s ', name)
        yield_dict[name] = calc_yields(
            db,
            sr=signal_regions[name],
            xsec=(1000.0 * xsec),
            lumi=luminosity_for_background
        )

    return yield_dict

def calc_yields(db, sr, xsec, lumi):

    data = np.zeros((5,2))
    for i in range(5):
        LOGGER.debug('calculating efficiency for %d top events', i)
        where = 'ntop = {}'.format(i)
        query = 'SELECT count(*) FROM dataset WHERE {}'.format(where)
        LOGGER.debug('calculating total number of %d top events', i)
        LOGGER.debug('query: %s', query)
        tot, = db.execute(query)
        tot = float(tot[0])
        LOGGER.debug('query returned %d', tot)

        query += ' AND {}'.format(sr)
        LOGGER.debug('calculating number of events in SR for %d top events', i)
        LOGGER.debug('query: %s', query)
        passd, = db.execute(query)
        passd = float(passd[0])
        LOGGER.debug('query returned %d', passd)

        eff = passd / tot if tot > 0 else 0
        assert eff <= 1, 'efficiency > 1!'
        u_eff = np.sqrt(eff*(1 - eff)/tot) if tot > 0 else 0
        LOGGER.debug('efficiency: %f +- %f', eff, u_eff)


        eff *= xsec
        eff *= lumi
        u_eff *= xsec
        u_eff *= lumi
        LOGGER.debug('scaling to xsec = %f', xsec)
        LOGGER.debug('scaling to luminosity = %f', lumi)
        LOGGER.debug('total number of events in SR: %f +- %f', eff, u_eff)

        data[i,0] = eff
        data[i,1] = u_eff

    return data
