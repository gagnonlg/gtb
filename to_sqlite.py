from __future__ import print_function

import argparse
import itertools as it
from math import cos, sqrt
import os
import sqlite3

import ROOT


GEV = 1.0/1000

def init_ROOT():
    ROOT.gROOT.SetBatch()
    ROOT.gROOT.Macro('$ROOTCOREDIR/scripts/load_packages.C')
    assert ROOT.xAOD.Init().isSuccess()

def get_args():
    p = argparse.ArgumentParser()
    p.add_argument('tb_file')
    p.add_argument('output')
    return p.parse_args()

def get_data(path):
    tb_file = ROOT.TFile(path)
    tb_tree = ROOT.xAOD.MakeTransientTree(tb_file)
    return tb_file, tb_tree

def init_db(path):
    db = sqlite3.connect(path)
    db.execute('''CREATE TABLE dataset (
    ntop INTEGER,
    njet_30 INTEGER,
    njet_70 INTEGER,
    nlepton INTEGER,
    dphimin4j REAL,
    nb INTEGER,
    met REAL,
    meff4j REAL,
    mtb REAL,
    meff REAL,
    mjsum REAL,
    mt REAL
    )''')
    return db

def insert(db, ntop, njet30, njet70, nlepton, dphimin4j, nb, met, meff4j,
           mtb, meff, mjsum, mt):
    query = 'INSERT INTO dataset VALUES ({},{},{},{},{},{},{},{},{},{},{},{})'
    query = query.format(ntop, njet30, njet70, nlepton, dphimin4j,
                         nb, met, meff4j, mtb, meff, mjsum, mt)
    db.execute(query)


def event_loop(db, tb_tree):
    # Here we embed the whole loop in a try-except block, because for some
    # unknown reason it will attempt to load some entries in excess
    try:
        for i, event in enumerate(tb_tree):
            if i % 100 == 0:
                print('event {}/{}'.format(i, tb_tree.GetEntries()))

            analyze_event(event, db)

    except RuntimeError:
        # Just ignore the error as we've used all events
        return

def count_tops(event):
    return len([top for top in event.TruthTop
                if top.auxdata('int')('motherID') == 1000021])

def get_jet_pt_phi(event, pt_req=20):
    jets = []
    for jet in event.AntiKt4TruthJets:
        if (jet.pt() * GEV) > pt_req and abs(jet.eta()) < 2.8:
            jets.append((jet.pt()*GEV, jet.phi()))
    return sorted(jets, reverse=True)


def get_bjet_pt_phi(event):
    jets = []
    for jet in event.AntiKt4TruthJets:
        if (jet.pt() * GEV) > 20 and abs(jet.eta()) < 2.5 \
           and abs(jet.auxdata('int')('PartonTruthLabelID')) == 5:
            jets.append((jet.pt()*GEV, jet.phi()))
    return sorted(jets, reverse=True)


def get_lepton_pt_phi(event):
    leptons = []
    for lepton in it.chain(event.TruthElectrons, event.TruthMuons):
        # https://twiki.cern.ch/twiki/bin/view/AtlasProtected/MCTruthClassifier
        t = lepton.auxdata('unsigned int')('classifierParticleType')
        isprompt = (t == 2) or (t == 6)
        if (lepton.pt()*GEV) > 20 and abs(lepton.eta()) < 2.5 and isprompt:
            leptons.append((lepton.pt()*GEV, lepton.phi()))

    return sorted(leptons, reverse=True)

def calc_dphimin4j(jets, met_phi):
    dphilist = []
    for (_, phi) in jets[:4]:
        dphilist.append(abs(phi - met_phi))
    return min(dphilist) if len(dphilist) > 0 else float('inf')


def calc_meff(jets, met, njets=None):
    if njets is None:
        njets = len(jets)
    meff = 0
    for i in range(min(njets, len(jets))):
        meff += jets[i][0]
    return meff + met


def calc_mtb(bjets, met):
    mtblist = []
    for (pt, phi) in bjets[:3]:
        mtblist.append(sqrt(2*pt*(met.met()*GEV)*
                            (1 - cos(phi - met.phi()))))
    return min(mtblist) if len(mtblist) > 0 else 0

def calc_mjsum(event):
    mjsum = 0
    largejetpt = [(j.pt(), j.eta(), j.m()) for j
                  in event.TrimmedAntiKt10TruthJets]
    for (pt, eta, m) in sorted(largejetpt, reverse=True)[:4]:
        if (pt*GEV) > 100 and abs(eta) < 2.0:
            mjsum += (m * GEV)
    return mjsum


def calc_mt(leptons, met):
    mt = 0
    if len(leptons) > 0:
        leading = leptons[0]
        mt = sqrt(2*leading[0]*(met.met()*GEV)*
                  (1 - cos(leading[1] - met.phi())))
    return mt


def analyze_event(event, db):

    jets = get_jet_pt_phi(event)
    bjets = get_bjet_pt_phi(event)
    leptons = get_lepton_pt_phi(event)
    met = event.MET_Truth['NonInt']

    insert(
        db=db,
        ntop=count_tops(event),
        njet30=len(get_jet_pt_phi(event, 30)),
        njet70=len(get_jet_pt_phi(event, 70)),
        nlepton=len(leptons),
        dphimin4j=calc_dphimin4j(jets, met.phi()),
        nb=len(bjets),
        met=(met.met()*GEV),
        meff4j=calc_meff(jets, met.met()*GEV, njets=4),
        mtb=calc_mtb(bjets, met),
        meff=calc_meff(jets, met.met()*GEV),
        mjsum=calc_mjsum(event),
        mt=calc_mt(leptons, met),
    )


def close_database(db):
    db.commit()
    db.close()


def main():
    init_ROOT()
    args = get_args()
    tb_file, tb_tree = get_data(args.tb_file)
    db = init_db(args.output)
    event_loop(db, tb_tree)
    close_database(db)


if __name__ == '__main__':
    main()
    os._exit(0)
