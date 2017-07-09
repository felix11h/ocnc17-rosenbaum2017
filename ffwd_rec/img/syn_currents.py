
import matplotlib
#matplotlib.style.use('classic')
matplotlib.use('Agg')
import matplotlib.pyplot as pl

import numpy as np
from brian2.units import *

import pickle,sys


if sys.argv[1]=='large':
    fname005 = "rb_arec0.05_N50000_T10000ms"
    fname025 = "rb_arec0.25_N50000_T10000ms"
    mode = 'large'
else:
    fname005 = "red_arec0.05_N4993_T10000ms"
    fname025 = "red_arec0.25_N4993_T10000ms"
    mode = 'small'
    
matplotlib.rc('text', usetex=True)
pl.rcParams['text.latex.preamble'] = [
    r'\usepackage{tgheros}',    
    r'\usepackage[eulergreek]{sansmath}',   
    r'\sansmath'                
    r'\usepackage{siunitx}',    
    r'\sisetup{detect-all}',    
]  

with open('../data/'+fname025+'.p', 'rb') as pfile:
    state025 = pickle.load(pfile)

with open('../data/'+fname005+'.p', 'rb') as pfile:
    state005 = pickle.load(pfile)

    
fig,ax = pl.subplots(2,1)
fig.set_size_inches(4.,5.)

state = state005
Erec = state['Erec']

burn_t = 2000*ms
bins = 200
n_traces = 3

Ie_syn = np.concatenate([Erec['Ie_syn'][:,k][Erec['t']>burn_t]/mV+Erec['If_syn'][:,k][Erec['t']>burn_t]/mV for k in range(n_traces)])

f, edges = np.histogram(Ie_syn, bins=bins, density=True)
bcs = 0.5*(edges[1:]+edges[:-1])
ax[0].plot(bcs, f, linewidth=3)

Ii_syn = np.concatenate([Erec['Ii_syn'][:,k][Erec['t']>burn_t]/mV for k in range(n_traces)])

f, edges = np.histogram(Ii_syn, bins=bins, density=True)
bcs = 0.5*(edges[1:]+edges[:-1])
ax[0].plot(bcs, f, linewidth=3)

Iall_syn = np.concatenate([Erec['Ie_syn'][:,k][Erec['t']>burn_t]/mV+Erec['If_syn'][:,k][Erec['t']>burn_t]/mV+Erec['Ii_syn'][:,k][Erec['t']>burn_t]/mV for k in range(n_traces)])

f, edges = np.histogram(Iall_syn, bins=bins, density=True)
bcs = 0.5*(edges[1:]+edges[:-1])
ax[0].plot(bcs, f, linewidth=3, color='gray')

ax[0].set_title(r'$\alpha_{\text{rec}} = 0.05$')
ax[0].set_xlabel('synaptic input [mV]')
ax[0].set_ylabel('probability density')

if mode=='small':
    ax[0].set_xlim((-40,40))
if mode=='large':
    ax[0].set_xlim((-175,75))

state = state025
Erec = state['Erec']

burn_t = 2000*ms
bins = 500
n_traces = 3

Ie_syn = np.concatenate([Erec['Ie_syn'][:,k][Erec['t']>burn_t]/mV+Erec['If_syn'][:,k][Erec['t']>burn_t]/mV for k in range(n_traces)])

f, edges = np.histogram(Ie_syn, bins=bins, density=True)
bcs = 0.5*(edges[1:]+edges[:-1])
ax[1].plot(bcs, f, linewidth=3)

Ii_syn = np.concatenate([Erec['Ii_syn'][:,k][Erec['t']>burn_t]/mV for k in range(n_traces)])

f, edges = np.histogram(Ii_syn, bins=bins, density=True)
bcs = 0.5*(edges[1:]+edges[:-1])
ax[1].plot(bcs, f, linewidth=3)

Iall_syn = np.concatenate([Erec['Ie_syn'][:,k][Erec['t']>burn_t]/mV+Erec['If_syn'][:,k][Erec['t']>burn_t]/mV+Erec['Ii_syn'][:,k][Erec['t']>burn_t]/mV for k in range(n_traces)])

f, edges = np.histogram(Iall_syn, bins=bins, density=True)
bcs = 0.5*(edges[1:]+edges[:-1])
ax[1].plot(bcs, f, linewidth=3, color='gray')

ax[1].set_title(r'$\alpha_{\text{rec}} = 0.25$')
ax[1].set_xlabel('synaptic input [mV]')
ax[1].set_ylabel('probability density')

if mode=='small':
    ax[1].set_xlim((-40,40))
if mode=='large':
    ax[1].set_xlim((-175,75))



for axs in ax:
    axs.spines['right'].set_visible(False)
    axs.spines['top'].set_visible(False)
    axs.yaxis.set_ticks_position('left')
    axs.xaxis.set_ticks_position('bottom')

pl.tight_layout(h_pad=3.25)
fig.savefig('syn_currents_{:s}.png'.format(mode), dpi=300) #bbox_inches='tight')





