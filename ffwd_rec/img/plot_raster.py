
import matplotlib
#matplotlib.style.use('classic')
matplotlib.use('Agg')
import matplotlib.pyplot as pl

import numpy as np
from brian2.units import *
from utils import get_spks

import pickle,sys

large=False
if sys.argv[1]=='large':
    fname005 = "rb_arec0.05_N50000_T10000ms"
    fname025 = "rb_arec0.25_N50000_T10000ms"
    large=True
else:
    fname005 = "red_arec0.05_N4993_T10000ms"
    fname025 = "red_arec0.25_N4993_T10000ms"

    
matplotlib.rc('text', usetex=True)
pl.rcParams['text.latex.preamble'] = [
    r'\usepackage{tgheros}',    
    r'\usepackage[eulergreek]{sansmath}',   
    r'\sansmath'                
    r'\usepackage{siunitx}',    
    r'\sisetup{detect-all}',    
]  


fig, ax = pl.subplots(2,1)
fig.set_size_inches(6,5.5)



with open('../data/'+fname025+'.p', 'rb') as pfile:
    state = pickle.load(pfile)
    Erec = state['Erec']
    Irec = state['Irec']
    espk = state['ESPK']
    ispk = state['ISPK']

size = 400 
tmin = 9000*ms
tmax = 10000*ms

Ne, Ni = len(state['NErcr']['x']), len(state['NIrcr']['x'])
Ne_slct = np.random.choice(np.arange(Ne), size, replace=False)
Ni_slct = np.random.choice(np.arange(Ni), size, replace=False)

ax[0].plot(*get_spks(espk, tmin, tmax, Ne_slct), 
           marker='.', color='blue', markersize=.5,
           linestyle='None')

ispk_t, ispk_id = get_spks(ispk, tmin, tmax, Ni_slct) 
ax[0].plot(ispk_t, ispk_id + size, 
           marker='.', color='red', markersize=.5,
           linestyle='None')

ax[0].margins(0.0)
ax[0].set_xlabel('t [ms]')
ax[0].set_ylabel('index i')
ax[0].set_title(r'$\alpha_{\mathrm{rec}} = 0.25$')

with open('../data/'+fname005+'.p', 'rb') as pfile:
    state = pickle.load(pfile)
    Erec = state['Erec']
    Irec = state['Irec']
    espk = state['ESPK']
    ispk = state['ISPK']

size = 400 
tmin = 9000*ms
tmax = 10000*ms

Ne, Ni = len(state['NErcr']['x']), len(state['NIrcr']['x'])
Ne_slct = np.random.choice(np.arange(Ne), size, replace=False)
Ni_slct = np.random.choice(np.arange(Ni), size, replace=False)

ax[1].plot(*get_spks(espk, tmin, tmax, Ne_slct), 
           marker='.', color='blue', markersize=.5,
           linestyle='None')

ispk_t, ispk_id = get_spks(ispk, tmin, tmax, Ni_slct) 
ax[1].plot(ispk_t, ispk_id + size, 
           marker='.', color='red', markersize=.5,
           linestyle='None')


ax[1].margins(0.0)
ax[1].set_xlabel('t [ms]')
ax[1].set_ylabel('index i')
ax[1].set_title(r'$\alpha_{\mathrm{rec}} = 0.05$')

pl.tight_layout()
fig.savefig('rnd_raster.png', dpi=300)



