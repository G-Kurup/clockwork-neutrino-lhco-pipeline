generate p p > l- l+ l- vl~ QCD=99 QED=99
add process p p > l- l+ l+ vl QCD=99 QED=99
output clockwork_bkg_lvl_100_TeV
launch
shower=PYTHIA8
delphes=ON
set nevents 100000
set ebeam1 50000.0
set ebeam2 50000.0
set cut_decays True
set ptj 50.0
set ptl 50.0
set mmjj 70.0
set mmjjmax 90.0
