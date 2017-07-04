
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pl

from brian2.units import *

import pickle

with open('../data/blncd_net_N2000_T20000ms.p', 'rb') as pfile:
    vi = pickle.load(pfile)
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


fig = pl.figure()
fig.set_size_inches(4,3.)

Ts = 19500*ms

ax = fig.add_subplot(1,1,1)
ax.set_xlabel('t [s]')
ax.set_ylabel('V [mV]')
ax.plot(vi['t'][vi['t']>Ts],
        vi['V'].T[3][vi['t']>Ts]/mV)

fig.savefig('name.png', dpi=300, bbox_inches='tight')


