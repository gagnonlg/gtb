import ROOT
from root_graph_utils import compare_histograms, hist_utils


gtb_file = ROOT.TFile('./hists_gtb.root')

hist1 = gtb_file.Get('h_2a_largejet_m')
hist1.Scale(1.0/hist1.Integral())
hist2 = gtb_file.Get('h_2b_largejet_m')
hist2.Scale(1.0/hist2.Integral())

hist3_ = [gtb_file.Get('h_{}_largejet_m'.format(k)) for k in ['1','2a','2b','3']]
hist3 = hist3_[0]
for h in hist3_[1:]:
    hist3.Add(h)
hist3.Scale(1.0/hist3.Integral())

hist4 = gtb_file.Get('h_1_largejet_m')
hist4.Scale(1.0/hist4.Integral())

hist5 = gtb_file.Get('h_3_largejet_m')
hist5.Scale(1.0/hist5.Integral())


def total_hist(variable):
    key = 'h_{}_' + variable
    hlist = [gtb_file.Get(key.format(i)) for i in ['1','2a','2b','3']]
    hist = hlist[0]
    for h in hlist[1:]:
        hist.Add(h)
    return hist

def get_hists(variable):
    key = 'h_{}_' + variable
    hists = [gtb_file.Get(key.format(i)) for i in ['1','2a','2b','3']]
    hists.append(total_hist(variable))
    for h in hists:
        hist_utils.normalize(h)
    labels = ['tb/bb+bb/tb','tb/tb','tt/bb+bb/tt','tt/tb+tb/tt', 'all']
    return hists, labels

def graph(variable, title, xlims=None, ylims=None, rebin=1, log=False):
    hists,labels = get_hists(variable)
    compare_histograms.from_hists(
        hists=hists[0:4],
        labels=labels[0:4],
        output='{}.pdf'.format(variable),
        xlims=xlims,
        ylims=ylims,
        title=title,
        geom='rectangle',
        rebin=rebin,
        log=log,
    )


graph(
    variable='jet_pt',
    title=';p_{T} [GeV]; Fraction of jets',
    log=True,
    xlims=(0,1400),
    ylims=(0.001, 0.5),
    rebin=4
)

graph(
    variable='jet_eta',
    title=';|#eta|; Fraction of jets',
    log=True,
    xlims=(0,3),
    ylims=(0.01, 0.5),
    rebin=4
)

graph(
    variable='jet_phi',
    title=';#phi; Fraction of jets',
    xlims=(0,3.5),
    rebin=10
)

graph(
    variable='jet_n',
    title=';N_{jet}; Fraction of events',
    log=True,
    ylims = (0.001, 0.5),
)

graph(
    variable='bjet_pt',
    title=';p_{T} [GeV]; Fraction of b-jets',
    log=True,
    xlims=(0,1400),
    ylims=(0.001, 0.5),
    rebin=4
)

graph(
    variable='bjet_eta',
    title=';|#eta|; Fraction of b-jets',
    log=True,
    xlims=(0,3),
    ylims=(0.01, 0.5),
    rebin=4
)

graph(
    variable='bjet_phi',
    title=';#phi; Fraction of b-jets',
    xlims=(0,3.5),
    rebin=10
)

graph(
    variable='bjet_n',
    title=';N_{b}; Fraction of events',
    log=True,
    ylims = (0.0001, 5),
    xlims=(0,10),
)


graph(
    variable='largejet_pt',
    title=';p_T [GeV]; Fraction of Large-R jets',
    xlims=(300, 1800),
    ylims=(0.001, 0.5),
    rebin=4,
    log=True,
)

graph(
    variable='largejet_eta',
    title=';|#eta|; Fraction of large-R jets',
    log=True,
    xlims=(0,2.5),
    ylims=(0.01, 0.5),
    rebin=4
)

graph(
    variable='largejet_phi',
    title=';#phi; Fraction of large-R jets',
    xlims=(0,3.5),
    rebin=10
)
graph(
    variable='largejet_m',
    title=';m [GeV];Fraction of large-R jets',
    xlims=(0,500),
    ylims=(0.001, 0.5),
    log=True,
)

graph(
    variable='largejet_n',
    title=';N_{Large-R jets};Fraction of Events',
    xlims=(0,10),
    log=True,
    ylims=(0.0001, 5)
)

graph(
    variable='largejet_n_m100',
    title=';N_{Large-R jets} w/ m > 100 GeV;Fraction of Events',
    xlims=(0,10),
    log=True,
    ylims=(0.0001, 5)
)

graph(
    variable='lepton_pt',
    title=';p_{T} [GeV]; Fraction of leptons',
    log=True,
    xlims=(0,1200),
    ylims=(0.001, 1),
    rebin=8
)

graph(
    variable='lepton_eta',
    title=';|#eta|; Fraction of leptons',
    log=True,
    xlims=(0,3),
    ylims=(0.001, 1),
    rebin=4
)

graph(
    variable='lepton_phi',
    title=';#phi; Fraction of leptons',
    xlims=(0,3.5),
    rebin=10
)

graph(
    variable='lepton_n',
    title=';N_{l}; Fraction of events',
    log=True,
    ylims = (0.001, 5),
    xlims=(0,6)
)

# TODO MET phi

graph(
    variable='MET_mag',
    title=';E_{T}^{miss};Fraction of events',
    rebin=10,
    log=True,
    ylims=(0.001,1)
)


# graph(
#     variable=,
#     title=,
# )
