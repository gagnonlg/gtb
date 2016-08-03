import argparse
import logging
import sqlite3

import numpy as np

import signal_regions


LOGGER = logging.getLogger('closure')


def get_args():
    args = argparse.ArgumentParser()
    args.add_argument('hard_coded')
    args.add_argument('to_reweight')
    return args.parse_args()


def parse_f_tt(path):
    end = path.split('_')[-1]
    number = '.'.join(end.split('.')[:2])
    return float(number)


def calc_branching_2(f_tt):
    f_bb = 1 - f_tt
    assert(np.isclose(f_tt + f_bb, 1))
    return np.array([
        f_bb * f_bb,
        0,
        f_tt * f_bb + f_bb * f_tt,
        0,
        f_tt * f_tt
    ])


def compatible(x, dx, y, dy):
    return (min(x+dx, y+dy) - max(x-dx, y-dy)) >= 0

def main():

    rc = 0

    logging.basicConfig(
        level=logging.INFO,
        format='[%(name)s] %(levelname)s %(message)s'
    )

    args = get_args()

    db_hc = sqlite3.connect(args.hard_coded)
    db_rw = sqlite3.connect(args.to_reweight)

    f_tt = parse_f_tt(args.hard_coded)
    LOGGER.info('f_tt = %f', f_tt)

    LOGGER.info('caculating yields')
    yields_hc = signal_regions.get_yields_dict(db_hc, 0.00276133)
    yields_rw = signal_regions.get_yields_dict(db_rw, 0.00276133)

    branching = calc_branching_2(f_tt)
    assert(np.isclose(1, np.sum(branching)))

    for sr in signal_regions.names:
        y_hc = yields_hc[sr]
        y_rw = yields_rw[sr]

        tot_hc = np.sum(branching*y_hc[:,0])
        unc_hc = np.sqrt(np.sum(branching*branching*y_hc[:,1]*y_hc[:,1]))
        LOGGER.info('total, hard_coded: %f +- %f', tot_hc, unc_hc)
        tot_rw = np.sum(y_rw[:,0] * branching)
        LOGGER.debug('y_rw: %s', str(y_rw))
        unc_rw = np.sqrt(np.sum(branching*branching*y_rw[:,1]*y_rw[:,1]))
        LOGGER.info('total, reweighted: %f +- %f', tot_rw, unc_rw)

        if compatible(tot_hc, 2*unc_hc, tot_rw, 2*unc_rw):
            LOGGER.info('SR=%s: PASS', sr)
        else:
            LOGGER.warning('SR=%s: FAIL', sr)
            rc = 1

    return rc

if __name__ == '__main__':
    exit(main())





# # yields_hc = get_yields_dict(db_hc, 1)
# # yields_rw = get_yields_dict(db_rw, 1)
# # branching = ...

# # compare that efficiency is the same
# # for sr in signal_regions.name:
# #     y_hc = yields_hc[sr]
# #     y_rw = yields_rw[sr]
# #     assert(np.isclose(np.sum(branching*y_rw), np.sum(y_hc)))
