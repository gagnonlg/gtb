import ROOT
from root_graph_utils import compare_histograms

file1 = ROOT.TFile('./hists_ggttbb.root')
file2 = ROOT.TFile('./hists_gtb.root')

hist1 = file1.Get('h_2_largejet_m')
hist1.Scale(1.0/hist1.Integral())
hist2 = file2.Get('h_2_largejet_m')
hist2.Scale(1.0/hist2.Integral())

compare_histograms.from_hists(
    hists=[hist1,hist2],
    labels=['ggttbb', 'gtb'],
    output='test.pdf',
)

# TODO xlims doesn,t work
