from __future__ import print_function
import argparse
import ROOT
import os.path

GEV = 1.0/1000

ROOT.gROOT.SetBatch()

ROOT.gROOT.Macro('$ROOTCOREDIR/scripts/load_packages.C')

p = argparse.ArgumentParser()
p.add_argument('tb_file')
p.add_argument('output')
args = p.parse_args()

ROOT.xAOD.Init().ignore()

tb_file = ROOT.TFile(args.tb_file)
tb_tree = ROOT.xAOD.MakeTransientTree(tb_file)
outfile = ROOT.TFile(args.output, 'RECREATE')

hists = {1: None, 2: None, 3: None}
for i in [1,2,3]:
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
        'MET_phi': ROOT.TH1D('h_{}_MET_phi'.format(i), '', 100, 0, 5),
        'MET_mag': ROOT.TH1D('h_{}_MET_mag'.format(i), '', 200, 0, 2000)
    }



event_dict = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}

met_min=float('inf')
met_max=-met_min

try:
    for i,event in enumerate(tb_tree):
        if i % 100 == 0:
            print('event {}/{}'.format(i,tb_tree.GetEntries()))
        ntops = len([top for top in event.TruthTop if top.auxdata('int')('motherID') == 1000021])
        event_dict[ntops] += 1

        # small-R jets and b-jets
        njets = 0
        nbjets = 0
        for jet in event.AntiKt4TruthJets:
            if (jet.pt() * GEV) > 20 and abs(jet.eta()) < 2.8:
                hists[ntops]['jet_pt'].Fill(jet.pt() * GEV)
                hists[ntops]['jet_eta'].Fill(abs(jet.eta()))
                hists[ntops]['jet_phi'].Fill(jet.phi())
                njets += 1
                if abs(jet.eta()) < 2.5 and abs(jet.auxdata('int')('PartonTruthLabelID')) == 5:
                    hists[ntops]['bjet_pt'].Fill(jet.pt() * GEV)
                    hists[ntops]['bjet_eta'].Fill(abs(jet.eta()))
                    hists[ntops]['bjet_phi'].Fill(jet.phi())
                    nbjets += 1

        hists[ntops]['jet_n'].Fill(njets)
        hists[ntops]['bjet_n'].Fill(nbjets)

        # large-R jets
        nlargejets = 0
        nlargejets_m100 = 0
        for jet in event.TrimmedAntiKt10TruthJets:
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

        # MET
        met = event.MET_Truth['NonInt']
        hists[ntops]['MET_phi'].Fill(met.phi())
        hists[ntops]['MET_mag'].Fill(met.met() * GEV)

except RuntimeError:
    pass

print(met_max)
print(met_min)

total = event_dict[0] + event_dict[1] + event_dict[2] + event_dict[3] + event_dict[4]
print('total: {}'.format(total))
for i in range(5):
    print('{}: {} ({}%)'.format(i, event_dict[i], 100 * event_dict[i] / float(total)))

outfile.Write()
