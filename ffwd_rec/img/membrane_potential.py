
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pl

import numpy as np
from brian2.units import *

import cPickle as pickle
import sys


if sys.argv[1]=='large':
    fname005 = "rb_arec0.05_N50000_T10000ms"
    fname025 = "rb_arec0.25_N50000_T10000ms"
    mode = 'large'
elif sys.argv[1]=='faulty':
    print "Attention! Using faulty data!"
    fname005 = "red_arec0.05_N4993_T10000ms_Vonly_faulty"
    fname025 = "red_arec0.25_N4993_T10000ms_Vonly_faulty"
    mode = 'faulty'
elif sys.argv[1]=='small':
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

    
fig,ax = pl.subplots(6,1)
fig.set_size_inches(4.,5.)

state = state005
Erec = state['Erec']

t_low = 9000*ms
t_high = 9500*ms

n_traces = 3

Vmin = 0
Vmax = -100

eVmax = 0
iVmax = 0

for k in range(n_traces):
    
    
    ts = Erec['t'][(Erec['t']>t_low) &(Erec['t']>t_high)]

    Vs = Erec['V'][:,k][(Erec['t']>t_low) &(Erec['t']>t_high)]/mV
    
    eVs = Erec['Ie_syn'][:,k][(Erec['t']>t_low) &(Erec['t']>t_high)]/mV+5
    iVs = Erec['Ii_syn'][:,k][(Erec['t']>t_low) &(Erec['t']>t_high)]/mV


    Vmin = np.min([Vmin, np.min(Vs)])
    
    eVmax = np.max([eVmax, np.max(abs(eVs))])
    iVmax = np.max([iVmax, np.max(abs(iVs))])

    ax[2*k].plot(ts,Vs, color='gray')
    
    ax[2*k+1].plot(ts,eVs)
    ax[2*k+1].plot(ts,iVs)



for j,axs in enumerate(ax):
    #axs.axis('off')
    axs.spines['left'].set_visible(True)
    axs.spines['right'].set_visible(False)
    axs.spines['top'].set_visible(False)
    axs.yaxis.set_ticks_position('left')
    axs.set_ylabel('[mV]')
    
    if not j==5:
        axs.spines['bottom'].set_visible(False)
        axs.xaxis.set_ticks_position('none')
        axs.xaxis.set_ticklabels([])
    else:
        axs.set_xlabel('time [s]')

    if j % 2 == 1:
        axs.set_ylim(-1*iVmax, eVmax)
    else:
        axs.set_ylim(Vmin, -10)

ax[0].set_title(r'$\alpha_{\text{rec}} = 0.05$')
        
pl.tight_layout(h_pad=1.25)
fig.savefig('memV_arec005_{:s}.png'.format(mode), dpi=300) #bbox_inches='tight')






fig,ax = pl.subplots(6,1)
fig.set_size_inches(4.,5.)

state = state025
Erec = state['Erec']

t_low = 9000*ms
t_high = 9500*ms

n_traces = 3

Vmin = 0
Vmax = -100

eVmax = 0
iVmax = 0

for k in range(n_traces):
    
    
    ts = Erec['t'][(Erec['t']>t_low) &(Erec['t']>t_high)]

    Vs = Erec['V'][:,k][(Erec['t']>t_low) &(Erec['t']>t_high)]/mV
    
    eVs = Erec['Ie_syn'][:,k][(Erec['t']>t_low) &(Erec['t']>t_high)]/mV+5
    iVs = Erec['Ii_syn'][:,k][(Erec['t']>t_low) &(Erec['t']>t_high)]/mV


    Vmin = np.min([Vmin, np.min(Vs)])
    
    eVmax = np.max([eVmax, np.max(abs(eVs))])
    iVmax = np.max([iVmax, np.max(abs(iVs))])

    ax[2*k].plot(ts,Vs, color='gray')
    
    ax[2*k+1].plot(ts,eVs)
    ax[2*k+1].plot(ts,iVs)



for j,axs in enumerate(ax):
    #axs.axis('off')
    axs.spines['left'].set_visible(True)
    axs.spines['right'].set_visible(False)
    axs.spines['top'].set_visible(False)
    axs.yaxis.set_ticks_position('left')
    axs.set_ylabel('[mV]')
    
    if not j==5:
        axs.spines['bottom'].set_visible(False)
        axs.xaxis.set_ticks_position('none')
        axs.xaxis.set_ticklabels([])
    else:
        axs.set_xlabel('time [s]')

    if j % 2 == 1:
        axs.set_ylim(-1*iVmax, eVmax)
    else:
        axs.set_ylim(Vmin, -10)

ax[0].set_title(r'$\alpha_{\mathrm{rec}} = 0.25$')
        
pl.tight_layout(h_pad=1.25)
fig.savefig('memV_arec025_{:s}.png'.format(mode), dpi=300) #bbox_inches='tight')
