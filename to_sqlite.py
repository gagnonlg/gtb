from __future__ import print_function
import argparse
import sqlite3

import ROOT
import os
import itertools as it
from math import cos,sqrt

GEV = 1.0/1000

ROOT.gROOT.SetBatch()

ROOT.gROOT.Macro('$ROOTCOREDIR/scripts/load_packages.C')

p = argparse.ArgumentParser()
p.add_argument('tb_file')
p.add_argument('output')
args = p.parse_args()

assert(ROOT.xAOD.Init().isSuccess())

tb_file = ROOT.TFile(args.tb_file)
tb_tree = ROOT.xAOD.MakeTransientTree(tb_file)

db = sqlite3.connect(args.output)
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
)'''
)

def insert(db, ntop, njet30, njet70, nlepton, dphimin4j, nb, met, meff4j,
           mtb, meff, mjsum, mt):
    query = 'INSERT INTO dataset VALUES ({},{},{},{},{},{},{},{},{},{},{},{})'
    query = query.format(ntop, njet30, njet70, nlepton, dphimin4j,
                         nb, met, meff4j, mtb, meff, mjsum, mt)
    db.execute(query)


# Here we embed the whole loop in a try-except block, because for some
# unknown reason it will attempt to load some entries in excess
try:
    for i,event in enumerate(tb_tree):
        if i % 100 == 0:
            print('event {}/{}'.format(i,tb_tree.GetEntries()))

        ntops = len([top for top in event.TruthTop
                     if top.auxdata('int')('motherID') == 1000021])

        # initialize variables to compute
        meff = 0
        meff4j = 0
        mt = 0


        # small-R jets and b-jets
        njet30 = 0
        njet70 = 0
        nbjets = 0
        jets = []
        bjets = []
        for jet in event.AntiKt4TruthJets:
            if (jet.pt() * GEV) > 20 and abs(jet.eta()) < 2.8:
                meff += (jet.pt() * GEV)
                if (jet.pt() * GEV) > 30:
                    njet30 += 1
                if (jet.pt() * GEV) > 70:
                    njet70 += 1
                jets.append((jet.pt()*GEV, jet.phi()))
                if abs(jet.eta()) < 2.5 and \
                   abs(jet.auxdata('int')('PartonTruthLabelID')) == 5:
                    bjets.append((jet.pt()*GEV, jet.phi()))
                    nbjets += 1

        # large-R jets
        mjsum = 0
        largejetpt = [(j.pt(),j.eta(),j.m()) for j
                      in event.TrimmedAntiKt10TruthJets]
        for (pt,eta,m) in sorted(largejetpt, reverse=True)[:4]:
            if (pt*GEV) > 100 and abs(eta) < 2.0:
                mjsum += (m * GEV)

        # leptons
        nleptons = 0
        leading = (-float('inf'), None)
        for lepton in it.chain(event.TruthElectrons, event.TruthMuons):
            # https://twiki.cern.ch/twiki/bin/view/AtlasProtected/MCTruthClassifier
            t = lepton.auxdata('unsigned int')('classifierParticleType')
            isprompt = (t == 2) or (t == 6)
            if (lepton.pt()*GEV) > 20 and abs(lepton.eta()) < 2.5 and isprompt:
                meff += (lepton.pt() * GEV)
                nleptons += 1
                if (lepton.pt() * GEV) > leading[0]:
                    leading = (lepton.pt() * GEV, lepton.phi())

        # MET
        met = event.MET_Truth['NonInt']

        meff += (met.met() * GEV)

        if nleptons > 0:
            mt = sqrt(2*leading[0]*(met.met()*GEV)*
                      (1 - cos(leading[1] - met.phi())))

        mtblist = []
        for (pt,phi) in sorted(bjets,reverse=True)[:3]:
            mtblist.append(sqrt(2*pt*(met.met()*GEV)*
                                (1 - cos(phi - met.phi()))))
        mtb = min(mtblist) if len(mtblist) > 0 else 0

        dphilist = []
        for (pt,phi) in sorted(jets, reverse=True)[:4]:
            dphilist.append(abs(phi - met.phi()))
            meff4j += pt # already in GEV
        meff4j += (met.met()*GEV)
        dphimin4j = min(dphilist)

        insert(
            db=db,
            ntop=ntops,
            njet30=njet30,
            njet70=njet70,
            nlepton=nleptons,
            dphimin4j=dphimin4j,
            nb=nbjets,
            met=(met.met()*GEV),
            meff4j=meff4j,
            mtb=mtb,
            meff=meff,
            mjsum=mjsum,
            mt=mt,
        )

except RuntimeError:
    # Just ignore the error as we've used all events
    pass


db.commit()
db.close()

# For some reason, even though everything is fine, ROOT will now
# segfault. To avoid this, we call os._exit directly
os._exit(0)
