from __future__ import print_function
import argparse
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
outfile = ROOT.TFile(args.output, 'RECREATE')

hists = {1: None, 2: None, 3: None}
for i in ['0', '1', '2a', '2b', '3', '4']:
    hists[i] = {
        'jet_pt': ROOT.TH1D('h_{}_jet_pt'.format(i), '', 200, 0,2000),
        'jet_eta': ROOT.TH1D('h_{}_jet_eta'.format(i), '', 100, 0, 5),
        'jet_phi': ROOT.TH1D('h_{}_jet_phi'.format(i), '', 100, 0, 5),
        'jet_n': ROOT.TH1D('h_{}_jet_n'.format(i), '', 20, 0, 20),
        'bjet_pt': ROOT.TH1D('h_{}_bjet_pt'.format(i), '', 200, 0,2000),
        'bjet_eta': ROOT.TH1D('h_{}_bjet_eta'.format(i), '', 100, 0, 5),
        'bjet_phi': ROOT.TH1D('h_{}_bjet_phi'.format(i), '', 100, 0, 5),
        'bjet_n': ROOT.TH1D('h_{}_bjet_n'.format(i), '', 20, 0, 20),
        'largejet_pt': ROOT.TH1D('h_{}_largejet_pt'.format(i), '', 200, 0,2000),
        'largejet_eta': ROOT.TH1D('h_{}_largejet_eta'.format(i), '', 100, 0, 5),
        'largejet_phi': ROOT.TH1D('h_{}_largejet_phi'.format(i), '', 100, 0, 5),
        'largejet_m': ROOT.TH1D('h_{}_largejet_m'.format(i), '', 200, 0, 2000),
        'largejet_n': ROOT.TH1D('h_{}_largejet_n'.format(i), '', 20, 0, 20),
        'largejet_n_m100': ROOT.TH1D('h_{}_largejet_n_m100'.format(i), '', 20, 0, 20),
        'lepton_pt': ROOT.TH1D('h_{}_lepton_pt'.format(i), '', 200, 0,2000),
        'lepton_eta': ROOT.TH1D('h_{}_lepton_eta'.format(i), '', 100, 0, 5),
        'lepton_phi': ROOT.TH1D('h_{}_lepton_phi'.format(i), '', 100, 0, 5),
        'lepton_n': ROOT.TH1D('h_{}_lepton_n'.format(i), '', 20, 0, 20),
        'MET_phi': ROOT.TH1D('h_{}_MET_phi'.format(i), '', 100, 0, 5),
        'MET_mag': ROOT.TH1D('h_{}_MET_mag'.format(i), '', 200, 0, 2000),
        'meff': ROOT.TH1D('h_{}_meff'.format(i), '', 500, 0, 5000),
        'mt': ROOT.TH1D('h_{}_mt'.format(i), '', 200, 0, 2000),
        'mtb': ROOT.TH1D('h_{}_mtb'.format(i), '', 200, 0, 2000),
        'dphimin4j': ROOT.TH1D('h_{}_dphimin4j'.format(i), '', 100, 0, 5),
        'mjsum': ROOT.TH1D('h_{}_mjsum'.format(i), '', 500, 0, 5000),
    }



event_dict = {'0': 0, '1': 0, '2a': 0, '2b': 0, '3': 0, '4': 0}

# Here we embed the whole loop in a try-except block, because for some
# unknown reason it will attempt to load some entries in excess
try:
    for i,event in enumerate(tb_tree):
        if i % 100 == 0:
            print('event {}/{}'.format(i,tb_tree.GetEntries()))

        # Classify the events by the number of tops TRUTH3 doesn't
        # keep the truth "chain" so we cannot separate
        # g->tt/g->bb from g->tb/g->tb
        ntops = str(len([top for top in event.TruthTop
                         if top.auxdata('int')('motherID') == 1000021]))
        if ntops == '2':
            if len([p for p in event.TruthBSM if p.absPdgId() == 1000024]) > 0:
                ntops += 'a'
            else:
                ntops += 'b'

        event_dict[ntops] += 1

        # initialize variables to compute
        meff = 0
        mt = 0


        # small-R jets and b-jets
        njets = 0
        nbjets = 0
        jets = []
        bjets = []
        for jet in event.AntiKt4TruthJets:
            if (jet.pt() * GEV) > 20 and abs(jet.eta()) < 2.8:
                hists[ntops]['jet_pt'].Fill(jet.pt() * GEV)
                hists[ntops]['jet_eta'].Fill(abs(jet.eta()))
                hists[ntops]['jet_phi'].Fill(jet.phi())
                meff += (jet.pt() * GEV)
                njets += 1
                jets.append((jet.pt()*GEV, jet.phi()))
                if abs(jet.eta()) < 2.5 and \
                   abs(jet.auxdata('int')('PartonTruthLabelID')) == 5:
                    hists[ntops]['bjet_pt'].Fill(jet.pt() * GEV)
                    hists[ntops]['bjet_eta'].Fill(abs(jet.eta()))
                    hists[ntops]['bjet_phi'].Fill(jet.phi())
                    bjets.append((jet.pt()*GEV, jet.phi()))
                    nbjets += 1

        hists[ntops]['jet_n'].Fill(njets)
        hists[ntops]['bjet_n'].Fill(nbjets)

        # large-R jets
        nlargejets = 0
        nlargejets_m100 = 0
        mjsum = 0
        nmj = 0
        for jet in event.TrimmedAntiKt10TruthJets:
            if (jet.pt()*GEV) > 100 and abs(jet.eta()) < 2.0 and nmj < 4:
                mjsum += (jet.m() * GEV)
                nmj += 1
            if (jet.pt()*GEV) > 300 and abs(jet.eta()) < 2.0:
                hists[ntops]['largejet_pt'].Fill(jet.pt() * GEV)
                hists[ntops]['largejet_eta'].Fill(abs(jet.eta()))
                hists[ntops]['largejet_phi'].Fill(jet.phi())
                hists[ntops]['largejet_m'].Fill(jet.m() * GEV)
                nlargejets += 1
                if (jet.m()*GEV) > 100:
                    nlargejets_m100 += 1

        hists[ntops]['largejet_n'].Fill(nlargejets)
        hists[ntops]['largejet_n_m100'].Fill(nlargejets_m100)
        hists[ntops]['mjsum'].Fill(mjsum)

        # leptons
        nleptons = 0
        leading = (-float('inf'), None)
        for lepton in it.chain(event.TruthElectrons, event.TruthMuons):
            # https://twiki.cern.ch/twiki/bin/view/AtlasProtected/MCTruthClassifier
            t = lepton.auxdata('unsigned int')('classifierParticleType')
            isprompt = (t == 2) or (t == 6)
            if (lepton.pt()*GEV) > 20 and abs(lepton.eta()) < 2.5 and isprompt:
                hists[ntops]['lepton_pt'].Fill(lepton.pt() * GEV)
                hists[ntops]['lepton_eta'].Fill(abs(lepton.eta()))
                hists[ntops]['lepton_phi'].Fill(lepton.phi())
                meff += (lepton.pt() * GEV)
                nleptons += 1
                if (lepton.pt() * GEV) > leading[0]:
                    leading = (lepton.pt() * GEV, lepton.phi())
        hists[ntops]['lepton_n'].Fill(nleptons)

        # MET
        met = event.MET_Truth['NonInt']
        hists[ntops]['MET_phi'].Fill(met.phi())
        hists[ntops]['MET_mag'].Fill(met.met() * GEV)

        meff += (met.met() * GEV)
        hists[ntops]['meff'].Fill(meff)

        if nleptons > 0:
            mt = sqrt(2*leading[0]*(met.met()*GEV)*
                      (1 - cos(leading[1] - met.phi())))
            hists[ntops]['mt'].Fill(mt)

        mtblist = []
        for (pt,phi) in sorted(bjets,reverse=True)[:3]:
            mtblist.append(sqrt(2*pt*(met.met()*GEV)*
                                (1 - cos(phi - met.phi()))))
        if len(mtblist) == 3:
            hists[ntops]['mtb'].Fill(min(mtblist))

        dphilist = []
        for (_,phi) in sorted(jets, reverse=True)[:4]:
            dphilist.append(abs(phi - met.phi()))
        if len(dphilist) == 4:
            hists[ntops]['dphimin4j'].Fill(min(dphilist))

except RuntimeError:
    # Just ignore the error as we've used all events
    pass


# check the yield
total = event_dict['0'] + \
        event_dict['1'] + \
        event_dict['2a'] + \
        event_dict['2b'] + \
        event_dict['3'] + \
        event_dict['4']

print('total: {}'.format(total))

for i in ['0','1','2a','2b','3','4']:
    print('{}: {} ({}%)'.format(
        i,
        event_dict[i],
        100 * event_dict[i] / float(total)
    ))


# finally, write the outfile
outfile.Write()

# For some reason, even though everything is fine, ROOT will now
# segfault. To avoid this, we call os._exit directly
os._exit(0)
