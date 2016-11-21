set -o errexit
python2 gen_spreadsheet.py > Gtb_request.csv
mkdir Gtb_request
cd Gtb_request
python2 ../gen_joboptions.py
cp ../param_card.SM.GG.tb.dat .
cp ../MadGraphControl_SimplifiedModel_GG_tb.py .
cd ..
tar cpzf Gtb_request{.tar.gz,}
