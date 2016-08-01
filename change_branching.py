import argparse

args = argparse.ArgumentParser()
args.add_argument('f_tt', type=float)
args = args.parse_args()

def format_gluino_decays(f_tt):

    s1 = '     %(f_tt)E    3     1000022         6        -6   # BR(~g -> ~chi_10 t  tb)\n' % \
         {'f_tt': f_tt}
    s2 = '     %(f_bb)E    3     1000022         5        -5   # BR(~g -> ~chi_10 b  bb)\n' % \
         {'f_bb': 1 - f_tt}

    return [s1,s2]


with open('param_card.SM.GG.ttbb.dat', 'r') as data_file:
    lines = data_file.readlines()

new_file=''.join(lines[:283] + format_gluino_decays(args.f_tt) + lines[285:])

with open('param_card.SM.GG.ttbb.dat', 'w') as data_file:
    data_file.write(new_file)

