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