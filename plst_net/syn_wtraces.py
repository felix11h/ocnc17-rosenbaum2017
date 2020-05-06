
import matplotlib
#matplotlib.style.use('classic')
matplotlib.use('Agg')
import matplotlib.pyplot as pl

import numpy as np
from brian2.units import mV, second, ms

import sys, pickle

with open('data/plst_net_red_arec0.25_affwd0.10_N4993_T50000ms_stdphom_selfrm.p', 'rb') as pfile:

    states005 = pickle.load(pfile)

states = states005


matplotlib.rc('text', usetex=True)
pl.rcParams['text.latex.preamble'] = [
    r'\usepackage{tgheros}',    
    r'\usepackage[eulergreek]{sansmath}',   
    r'\sansmath'                
    r'\usepackage{siunitx}',    
    r'\sisetup{detect-all}',    
]  



fig,ax = pl.subplots(1,1)
fig.set_size_inches(5.,3.5)

t = states['SEERec']['t']
ws = states['SEERec']['w']

for k in range(5):
    ax.plot(t/second, ws[:,k]/mV)

ax.set_xlabel('time [s]')
ax.set_ylabel('synaptic weight [mV]')

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')


fig.tight_layout()
fig.savefig('img/syn_wtraces.png', dpi=300) #b
