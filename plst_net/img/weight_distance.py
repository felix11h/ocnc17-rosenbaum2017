
import matplotlib
#matplotlib.style.use('classic')
matplotlib.use('Agg')
import matplotlib.pyplot as pl

import numpy as np
from brian2.units import *

import cPickle as pickle
import sys


# with open('../data/plst_net_red_arec0.05_N4993_T50000ms_stdphom_selfrm.p', 'rb') as pfile:
#     st005_010 = pickle.load(pfile)
#     st005_010.update({'a_rec': 0.05, 'a_ffwd': 0.10})
# with open('../data/plst_net_red_arec0.25_N4993_T50000ms_stdphom_selfrm.p', 'rb') as pfile:
#     st025_010 = pickle.load(pfile)
#     st025_010.update({'a_rec': 0.25, 'a_ffwd': 0.10})

# with open('../data/plst_net_red_arec0.10_affwd0.20_N4993_T50000ms_stdphom_selfrm.p', 'rb') as pfile:
#     st010_020 = pickle.load(pfile)
#     st010_020.update({'a_rec': 0.10, 'a_ffwd': 0.20})
# with open('../data/plst_net_red_arec0.50_affwd0.20_N4993_T50000ms_stdphom_selfrm.p', 'rb') as pfile:
#     st050_020 = pickle.load(pfile)
#     st050_020.update({'a_rec': 0.50, 'a_ffwd': 0.20})
    
# with open('../data/plst_net_red_arec0.10_affwd0.15_N4993_T50000ms_stdphom_selfrm.p', 'rb') as pfile:
#     st010_015 = pickle.load(pfile)
#     st010_015.update({'a_rec': 0.10, 'a_ffwd': 0.15})
# with open('../data/plst_net_red_arec0.30_affwd0.15_N4993_T50000ms_stdphom_selfrm.p', 'rb') as pfile:
#     st030_015 = pickle.load(pfile)
#     st030_015.update({'a_rec': 0.30, 'a_ffwd': 0.15})

    
matplotlib.rc('text', usetex=True)
pl.rcParams['text.latex.preamble'] = [
    r'\usepackage{tgheros}',    
    r'\usepackage[eulergreek]{sansmath}',   
    r'\sansmath'                
    r'\usepackage{siunitx}',    
    r'\sisetup{detect-all}',    
]  



def make_figure(sets):
    
    fig,ax = pl.subplots(1,1)
    fig.set_size_inches(5.,3.5)

    for dat in sets:

        NE= dat['NErcr']
        See = dat['S_ee']

        dists = [np.sqrt((abs(NE['x'][See['i'][k]] - NE['x'][See['j'][k]]) % 32)**2 + (abs(NE['y'][See['i'][k]] - NE['y'][See['j'][k]]) % 32)**2) for k in range(len(See['i']))]

        n, dbins = np.histogram(dists, bins=50)
        sy, _  = np.histogram(dists, bins=dbins, weights=See['w']/mV)
        sy2, _  = np.histogram(dists, bins=dbins, weights=See['w']/mV*See['w']/mV)

        centers = 0.5*(dbins[1:]+dbins[:-1])

        ax.plot(centers, sy/n, label=r'$\alpha_{\text{rec}} ='+str(dat['a_rec']) + '$, '+ r'$\alpha_{\text{ffwd}} = ' + str(dat['a_ffwd']) +'$', linewidth=3.)


    ax.set_xlabel('distance [a.u.]')
    ax.set_ylabel('mean synaptic weight [mV]')
        
    ax.legend(loc='upper right', framealpha=1., frameon=False)

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')

    pl.tight_layout()
    fig.savefig('set1.png', dpi=300) #bbox_inches='tight')





if __name__ == '__main__':

    make_figure([st005_010])



