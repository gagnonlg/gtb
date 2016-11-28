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
args = p.parse_args()

assert(ROOT.xAOD.Init().isSuccess())

tb_file = ROOT.TFile(args.tb_file)
tb_tree = ROOT.xAOD.MakeTransientTree(tb_file)


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

        # if ntops not in ['1', '3']:
        #     print("*** ntops == {}".format(ntops))
        #     #tops = [top for top in event.TruthTop if top.auxdata('int')('motherID') == 1000021]
        #     tops = event.TruthTop
        #     for k,t in enumerate(tops):
        #         print('----> top {}'.format(k))
        #         print('pdgId == {}'.format(t.pdgId()))
        #         print('motherId ==  {}'.format(t.auxdata('int')('motherID')))
        #         print('barcode == {}'.format(t.barcode()))
        #         print('status == {}'.format(t.status()))
        #         print('pt == {}'.format(t.pt()))
        #         print('eta == {}'.format(t.eta()))
        #         print('e == {}'.format(t.e()))

 

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

# For some reason, even though everything is fine, ROOT will now
# segfault. To avoid this, we call os._exit directly
os._exit(0)
