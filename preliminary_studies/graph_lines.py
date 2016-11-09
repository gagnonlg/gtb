import argparse

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def get_args():
    args = argparse.ArgumentParser()
    args.add_argument('--output', required=True)
    args.add_argument('--inputs', nargs='+', required=True)
    return args.parse_args()


def main():
    args = get_args()
    plt.figure(num=None, figsize=(8, 6), dpi=200, facecolor='w', edgecolor='k')
    maxes = []
    for path in args.inputs:
        data = np.loadtxt(path)
        label = '_'.join(path.split('_')[4:]).split('.')[0]

        if 'gbb' in label:
            style='-'
        if 'gtt_0l' in label:
            style='--'
        if 'gtt_1l' in label:
            style='-.'

        if 'A' in label:
            style = 'k' + style
        if 'B' in label:
            style = 'r' + style
        if 'C' in label:
            style = 'g' + style


        plt.plot(data[:,0], data[:,1], style, label=label, linewidth=2)
        maxes.append(np.max(data[:,1]))

    m_g = args.inputs[0].split('_')[0]
    m_l = args.inputs[0].split('_')[2]
    ymax = max(maxes)*1.2
    plt.text(0.02, ymax-0.5, "m_g = {}, m_l = {}".format(m_g,m_l))


    plt.xlabel('f_tt')
    plt.ylabel('significance')
    plt.legend(loc='best', fontsize='small')
    plt.axis([0,1,-1,ymax])
    plt.savefig(args.output)
    plt.close()

if __name__ == '__main__':
    exit(main())

