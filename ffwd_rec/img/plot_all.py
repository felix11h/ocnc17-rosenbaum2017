
import matplotlib
#matplotlib.style.use('classic')
matplotlib.use('Agg')
import matplotlib.pyplot as pl

import numpy as np
from brian2.units import *

import pickle

# with open('../data/blncd_net_N2000_T20000ms.p', 'rb') as pfile:
#     vi = pickle.load(pfile)
#     espk = pickle.load(pfile)
#     ispk = pickle.load(pfile)

#with open('../data/ffwd_rec_N4993_T10000ms.p', 'rb') as pfile:
#with open('../data/rb_arec0.25_N50000_T10000ms_nofix.p', 'rb') as pfile:
# with open('../data/rb_arec0.25_N50000_T10000ms.p', 'rb') as pfile:
with open('../data/red_arec0.25_N4993_T10000ms.p', 'rb') as pfile:
    Erec = pickle.load(pfile)
    Irec = pickle.load(pfile)
    espk = pickle.load(pfile)
    ispk = pickle.load(pfile)


matplotlib.rc('text', usetex=True)
pl.rcParams['text.latex.preamble'] = [
    r'\usepackage{tgheros}',    # helvetica font
    r'\usepackage{sansmath}',   # math-font matching  helvetica
    r'\sansmath'                # actually tell tex to use it!
    r'\usepackage{siunitx}',    # micro symbols
    r'\sisetup{detect-all}',    # force siunitx to use the fonts
]  


fig,ax = pl.subplots(2,1)
fig.set_size_inches(5,5.5)

Ts = 9500*ms
k = 1

ax[0].set_xlabel('t [s]')
ax[0].set_ylabel('V [mV]')
ax[0].plot(Erec['t'][Erec['t']>Ts],
        Erec['V'].T[k][Erec['t']>Ts]/mV)
ax[0].margins(0.01)


ax[1].set_xlabel('t [s]')
ax[1].set_ylabel('V [mV]')
ax[1].plot(Erec['t'][Erec['t']>Ts],
           Erec['Ie_syn'].T[k][Erec['t']>Ts]/mV,
           label=r'$I^{\text{exc}}_{\text{syn}}$')
ax[1].plot(Erec['t'][Erec['t']>Ts],
           Erec['Ii_syn'].T[k][Erec['t']>Ts]/mV,
           label=r'$I^{\text{inh}}_{\text{syn}}$')
ax[1].plot(Erec['t'][Erec['t']>Ts],
           (Erec['Ie_syn'].T[k][Erec['t']>Ts] + \
            Erec['Ii_syn'].T[k][Erec['t']>Ts])/mV,
           color='gray',
           label=r'$I^{\text{inh}}_{\text{syn}}' +\
                 r' + I^{\text{inh}}_{\text{syn}}$')

yl=np.max(np.abs(pl.ylim()))
ax[1].set_ylim((-yl,yl))
ax[1].margins(0.01)

ax[1].legend(bbox_to_anchor=(0., 1.01, 1., .101),
             loc='lower center', framealpha=1., ncol=3,
             frameon=False)



pl.tight_layout(h_pad=3.25)
fig.savefig('name.png', dpi=300) #bbox_inches='tight')




fig, ax = pl.subplots(2,1)
fig.set_size_inches(6,5.5)

iN = 400
tmin = 9000*ms
ke = 0
ki = 0

ax[0].plot((espk['t'][(espk['t']>tmin) & (espk['i']<iN)]-tmin)/ms,
        espk['i'][(espk['t']>tmin) & (espk['i']<iN)],
        '.', color='blue', markersize=.5)
ax[0].plot((ispk['t'][(ispk['t']>tmin) & (ispk['i']<iN)]-tmin)/ms,
        iN+ispk['i'][(ispk['t']>tmin) & (ispk['i']<iN)],
        '.', color='red', markersize=.5)

ax[0].margins(0.0)
ax[0].set_xlabel('t [ms]')
ax[0].set_ylabel('index i')

# tmin = 19900*ms

# ax[1].plot((Erec['t'][Erec['t']>tmin]-tmin)/ms,
#            Erec['Iex'][Erec['t']>tmin]/mV,
#            color='blue')
# ax[1].plot((Irec['t'][Irec['t']>tmin]-tmin)/ms,
#            Irec['Iex'][Irec['t']>tmin]/mV,
#            color='red')

# ax[1].set_xlabel('t [ms]')
# ax[1].set_ylabel('external input [mV]')

pl.tight_layout()
fig.savefig('new.png', dpi=300)


# --------------------------------------

#load synapse S_ee, load NErcr
pl.scatter(NErcr.x, NErcr.y, s=1, c=np.bincount(S_ee.j))


