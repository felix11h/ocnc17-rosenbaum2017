
import matplotlib
#matplotlib.style.use('classic')
matplotlib.use('Agg')
import matplotlib.pyplot as pl

import numpy as np
from brian2.units import *

import pickle

with open('data/red_arec0.25_N4993_T10000ms.p', 'rb') as pfile:
    state = pickle.load(pfile)
    

matplotlib.rc('text', usetex=True)
pl.rcParams['text.latex.preamble'] = [
    r'\usepackage{tgheros}',    # helvetica font
    r'\usepackage{sansmath}',   # math-font matching  helvetica
    r'\sansmath'                # actually tell tex to use it!
    r'\usepackage{siunitx}',    # micro symbols
    r'\sisetup{detect-all}',    # force siunitx to use the fonts
]  

Ne = len(state['NErcr']['x'])
Ni = len(state['NIrcr']['x'])

print(len(state['NErcr']['x']),  len(state['NErcr']['y']), len(np.bincount(state['S_ee']['j'])))

fig, ax = pl.subplots(3,2)
fig.set_size_inches(6.,7.5)

ax[0,0].set_title('pop: NErcr, syn: NErcr')
ax[0,0].set_aspect('equal', 'datalim')
cm = pl.cm.get_cmap('RdYlBu')
sc = ax[0,0].scatter(state['NErcr']['x'], state['NErcr']['y'], s=1,
           c=np.bincount(state['S_ee']['j'], minlength=Ne), cmap=cm)
fig.colorbar(sc, ax=ax[0,0])


ax[0,1].set_title('pop: NIrcr, syn: NErcr')
ax[0,1].set_aspect('equal', 'datalim')
cm = pl.cm.get_cmap('RdYlBu')
sc = ax[0,1].scatter(state['NIrcr']['x'], state['NIrcr']['y'], s=10,
           c=np.bincount(state['S_ie']['j'], minlength=Ni), cmap=cm)
fig.colorbar(sc, ax=ax[0,1])


ax[1,0].set_title('pop: NErcr, syn: NIrcr')
ax[1,0].set_aspect('equal', 'datalim')
cm = pl.cm.get_cmap('RdYlBu')
sc = ax[1,0].scatter(state['NErcr']['x'], state['NErcr']['y'], s=1,
           c=np.bincount(state['S_ei']['j'], minlength=Ne), cmap=cm)
fig.colorbar(sc, ax=ax[1,0])


ax[1,1].set_title('pop: NIrcr, syn: NIrcr')
ax[1,1].set_aspect('equal', 'datalim')
cm = pl.cm.get_cmap('RdYlBu')
sc = ax[1,1].scatter(state['NIrcr']['x'], state['NIrcr']['y'], s=10,
           c=np.bincount(state['S_ii']['j'], minlength=Ni), cmap=cm)
fig.colorbar(sc, ax=ax[1,1])

ax[2,0].set_title('pop: NErcr, syn: Ffwd')
ax[2,0].set_aspect('equal', 'datalim')
cm = pl.cm.get_cmap('RdYlBu')
sc = ax[2,0].scatter(state['NErcr']['x'], state['NErcr']['y'], s=1,
           c=np.bincount(state['S_eF']['j']), cmap=cm)
fig.colorbar(sc, ax=ax[2,0])

ax[2,1].set_title('pop: NIrcr, syn: Ffwd')
ax[2,1].set_aspect('equal', 'datalim')
cm = pl.cm.get_cmap('RdYlBu')
sc = ax[2,1].scatter(state['NIrcr']['x'], state['NIrcr']['y'], s=10,
           c=np.bincount(state['S_iF']['j']), cmap=cm)
fig.colorbar(sc, ax=ax[2,1])



fig.tight_layout()
fig.savefig('img/plot_connectivty.png', dpi=300)




#load synapse S_ee, load NErcr



