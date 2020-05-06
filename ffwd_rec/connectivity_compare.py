
import matplotlib
#matplotlib.style.use('classic')
matplotlib.use('Agg')
import matplotlib.pyplot as pl

matplotlib.rc('text', usetex=True)
pl.rcParams['text.latex.preamble'] = [
    r'\usepackage{tgheros}',    # helvetica font
    r'\usepackage{sansmath}',   # math-font matching  helvetica
    r'\sansmath'                # actually tell tex to use it!
    r'\usepackage{siunitx}',    # micro symbols
    r'\sisetup{detect-all}',    # force siunitx to use the fonts
]  

import numpy as np
from brian2.units import *

import pickle

with open('data/red_arec0.25_N4993_T10000ms.p', 'rb') as pfile:
    state = pickle.load(pfile)

with open('data/red_arec0.05_N4993_T10000ms.p', 'rb') as pfile:
    cstate = pickle.load(pfile)

    

Ne = len(state['NErcr']['x'])
Ni = len(state['NIrcr']['x'])

print(len(state['NErcr']['x']),
      len(state['NErcr']['y']),
      len(np.bincount(state['S_ee']['j'])))

      
fig, ax = pl.subplots()
fig.set_size_inches(3.5,3)

ax.set_title('pop: NErcr, syn: NErcr')
ax.set_aspect('equal', 'datalim')
cm = pl.cm.get_cmap('RdYlBu')
sc = ax.scatter(state['NErcr']['x'], state['NErcr']['y'], s=2.,
           c=np.bincount(state['S_ee']['j'], minlength=Ne), cmap=cm)
fig.colorbar(sc, ax=ax)


fig.tight_layout()
fig.savefig('img/connectivity_before.png', dpi=300)




fig, ax = pl.subplots()
fig.set_size_inches(3.5,3)

ax.set_title('pop: NErcr, syn: NErcr')
ax.set_aspect('equal', 'datalim')
cm = pl.cm.get_cmap('RdYlBu')
sc = ax.scatter(state['NErcr']['x'], state['NErcr']['y'], s=2.,
           c=np.bincount(state['S_ee']['j'], minlength=Ne), cmap=cm)
sc = ax.scatter(cstate['NErcr']['x'], cstate['NErcr']['y'], s=2.,
                c=np.bincount(cstate['S_ee']['j'], minlength=Ne), cmap=cm, vmin=0, vmax=550)
fig.colorbar(sc, ax=ax)


fig.tight_layout()
fig.savefig('img/connectivity_after.png', dpi=300)



#load synapse S_ee, load NErcr



