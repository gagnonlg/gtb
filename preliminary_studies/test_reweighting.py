import argparse
import itertools as it
import logging
import os
import sqlite3

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import ROOT

import signal_regions

LOGGER = logging.getLogger('test_reweighting')

UNCERT=0.3

significance = ROOT.RooStats.NumberCountingUtils.BinomialExpZ

def get_args():
    args = argparse.ArgumentParser()
    args.add_argument('--input', required=True)
    args.add_argument('--xsec', required=True, type=float)
    args.add_argument('--output', required=True)
    args.add_argument('--loglevel', default='INFO')
    return args.parse_args()


def get_yields_dict(db, xsec):
    yield_dict = {}
    for name in signal_regions.names:
        LOGGER.debug('calculating yields for region %s ', name)
        yield_dict[name] = calc_yields(
            db,
            sr=signal_regions.signal_regions[name],
            xsec=(1000.0 * xsec),
            lumi=signal_regions.luminosity_for_background
        )

    return yield_dict

def calc_yields(db, sr, xsec, lumi):

    data = np.zeros(5)
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

        eff = passd / tot
        assert eff <= 1, 'efficiency > 1!'
        LOGGER.debug('efficiency: %f', eff)

        eff *= xsec
        eff *= lumi
        LOGGER.debug('scaling to xsec = %f', xsec)
        LOGGER.debug('scaling to luminosity = %f', lumi)
        LOGGER.debug('total number of events in SR: %f', eff)

        data[i] = eff

    return data

def main():

    args = get_args()

    logging.basicConfig(
        level=args.loglevel,
        format='[%(name)s] %(levelname)s %(message)s'
    )

    LOGGER.debug('input: %s', args.input)
    LOGGER.debug('xsec: %f', args.xsec)
    LOGGER.debug('output: %s', args.output)

    if not os.path.exists(args.input):
        LOGGER.error('database "%s" does not exists', args.input)
        return 1

    db = sqlite3.connect(args.input)

    yields_dict = get_yields_dict(db, args.xsec)

    bkgnd_dict = signal_regions.backgrounds
    for k,v in bkgnd_dict.iteritems():
        LOGGER.debug('background yields at %f fb^-1:', signal_regions.luminosity_for_background)
        LOGGER.debug('%s: %f', k, v)

    for sr in signal_regions.names:
        LOGGER.info('calculating line in SR %s', sr)
        yields = yields_dict[sr]
        yield_bkgnd = bkgnd_dict[sr]
        line = calc_line(yields, yield_bkgnd)
        graph_line(line, sr, args.output)

        LOGGER.info('calculating triangle in SR %s', sr)
        triangle = calc_triangle(yields, yield_bkgnd)
        graph_triangle(triangle, sr, args.output)

def graph_line(line, sr, prefix):
    LOGGER.debug('plotting line for SR %s', sr)
    x,y = line
    plt.figure(num=None, figsize=(8, 6), dpi=200, facecolor='w', edgecolor='k')
    plt.plot(x,y)
    plt.xlabel('f_tt')
    plt.ylabel('significance')
    plt.title(sr)
    path = '{}_line_{}.png'.format(prefix, sr)
    plt.savefig(path)
    LOGGER.info('saved line in file %s', path)

    data = np.zeros((x.shape[0], 2))
    data[:,0] = x
    data[:,1] = y

    np.savetxt(path.replace('png','gz'), data)
    LOGGER.info('data saved in file %s', path.replace('png','gz'))

    plt.close()

def graph_triangle(triangle, sr, prefix):
    masked_data = np.ma.masked_equal(triangle.T, 0)
    plt.figure(num=None, figsize=(8, 6), dpi=200, facecolor='w', edgecolor='k')
    plt.imshow(masked_data, cmap='Reds')
    plt.xlabel('f_tt')
    plt.ylabel('f_bb')
    plt.axis([0,100,0,100])
    cb = plt.colorbar()
    cb.set_label('significance')

    plt.text(55, 95, sr)
    m_g = prefix.split('_')[0]
    m_l = prefix.split('_')[2]
    plt.text(55, 90, "m_g = {}, m_l = {}".format(m_g,m_l))

    path = '{}_triangle_{}.png'.format(prefix, sr)
    plt.savefig(path)
    LOGGER.info('saved triangle in file %s', path)


def calc_line(signals, bkgnd):
    f_tt = np.linspace(0, 1, 100)
    results = np.zeros_like(f_tt)
    for i, f in enumerate(f_tt):
        s = sr_yield(f, 1 - f, signals, include_1_3=False)
        results[i] = significance(s, bkgnd, UNCERT)
        LOGGER.debug('bkgnd: %f', bkgnd)
        LOGGER.debug('significane: %f', results[i])
    return f_tt, results

def calc_triangle(signals, bkgnd):
    n = 100
    f_tt = np.linspace(0, 1, n)
    f_bb = np.linspace(0, 1, n)
    results = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            tt = f_tt[i]
            bb = f_bb[j]
            if tt + bb <= 1:
                s = sr_yield(tt, bb, signals, include_1_3=True)
                results[i,j] = significance(s, bkgnd, UNCERT)
    return results

def sr_yield(f_tt, f_bb, yields, include_1_3=False):
    LOGGER.debug('calculating total yield for f_tt=%f and f_bb=%f', f_tt, f_bb)
    branching = calc_branching(f_tt, f_bb)
    LOGGER.debug('branching ratios: %s', str(branching))

    if not include_1_3:
        LOGGER.debug('Using the 2 branching ratios scenario')
        LOGGER.debug('Rescaling the branching ratios')
        branching[1] = 0
        branching[3] = 0
        branching /= np.sum(branching)
        LOGGER.debug('rescaled branching ratios: %s', str(branching))

    assert(np.isclose(1, np.sum(branching)))
    LOGGER.debug('yields, unscaled: %s', str(yields))
    assert(yields.shape == branching.shape)
    yields_scaled = yields * branching
    LOGGER.debug('yields: %s', str(yields_scaled))
    total = np.sum(yields_scaled)
    LOGGER.debug('total yield: %f', total)
    return total


def calc_branching(f_tt, f_bb):
    f_tb = 1 - f_tt - f_bb
    return np.array([
        f_bb * f_bb,
        f_bb * f_tb + f_tb * f_bb,
        f_bb * f_tt + f_tt * f_bb + f_tb * f_tb,
        f_tb * f_tt + f_tt * f_tb,
        f_tt * f_tt
    ])



if __name__ == '__main__':
    exit(main())

