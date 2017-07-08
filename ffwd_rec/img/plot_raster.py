
import matplotlib
#matplotlib.style.use('classic')
matplotlib.use('Agg')
import matplotlib.pyplot as pl

import numpy as np
from brian2.units import *

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
    r'\usepackage{tgheros}',    # helvetica font
    r'\usepackage{sansmath}',   # math-font matching  helvetica
    r'\sansmath'                # actually tell tex to use it!
    r'\usepackage{siunitx}',    # micro symbols
    r'\sisetup{detect-all}',    # force siunitx to use the fonts
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

Ne, Ni = len(state['NErcr']['x']), len(state['NIrcr']['x'])
Ne_slct = np.random.choice(np.arange(Ne), size, replace=False)
Ni_slct = np.random.choice(np.arange(Ni), size, replace=False)

remapE = np.ones(Ne)*-1
remapE[Ne_slct] = np.arange(len(Ne_slct))

ax[0].plot((espk['t'][(espk['t']>tmin) & (np.in1d(espk['i'],Ne_slct))]-tmin)/ms,
        remapE[espk['i'][(espk['t']>tmin) & (np.in1d(espk['i'],Ne_slct))]],
        '.', color='blue', markersize=.5)

remapI = np.ones(Ni)*-1
remapI[Ni_slct] = np.arange(len(Ni_slct))

ax[0].plot((ispk['t'][(ispk['t']>tmin) & (np.in1d(ispk['i'], Ni_slct))]-tmin)/ms,
        remapI[ispk['i'][(ispk['t']>tmin) & (np.in1d(ispk['i'],Ni_slct))]]+size,
        '.', color='red', markersize=.5)

ax[0].margins(0.0)
ax[0].set_xlabel('t [ms]')
ax[0].set_ylabel('index i')


with open('../data/'+fname005+'.p', 'rb') as pfile:
    state = pickle.load(pfile)
    Erec = state['Erec']
    Irec = state['Irec']
    espk = state['ESPK']
    ispk = state['ISPK']


iN = 400
size = 400 
tmin = 9000*ms

Ne, Ni = len(state['NErcr']['x']), len(state['NIrcr']['x'])
Ne_slct = np.random.choice(np.arange(Ne), size, replace=False)
Ni_slct = np.random.choice(np.arange(Ni), size, replace=False)

remapE = np.ones(Ne)*-1
remapE[Ne_slct] = np.arange(len(Ne_slct))

ax[1].plot((espk['t'][(espk['t']>tmin) & (np.in1d(espk['i'],Ne_slct))]-tmin)/ms,
        remapE[espk['i'][(espk['t']>tmin) & (np.in1d(espk['i'],Ne_slct))]],
        '.', color='blue', markersize=.5)

remapI = np.ones(Ni)*-1
remapI[Ni_slct] = np.arange(len(Ni_slct))

ax[1].plot((ispk['t'][(ispk['t']>tmin) & (np.in1d(ispk['i'], Ni_slct))]-tmin)/ms,
        remapI[ispk['i'][(ispk['t']>tmin) & (np.in1d(ispk['i'],Ni_slct))]]+size,
        '.', color='red', markersize=.5)

ax[1].margins(0.0)
ax[1].set_xlabel('t [ms]')
ax[1].set_ylabel('index i')

pl.tight_layout()
fig.savefig('rnd_raster.png', dpi=300)



