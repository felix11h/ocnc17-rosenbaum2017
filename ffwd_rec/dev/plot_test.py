
import matplotlib
#matplotlib.style.use('classic')
matplotlib.use('Agg')
import matplotlib.pyplot as pl

import numpy as np
from brian2.units import *

import pickle

# with open('../data/red_arec0.25_N4993_T10ms.p', 'rb') as pfile:
#     state = pickle.load(pfile)
    

matplotlib.rc('text', usetex=True)
pl.rcParams['text.latex.preamble'] = [
    r'\usepackage{tgheros}',    # helvetica font
    r'\usepackage{sansmath}',   # math-font matching  helvetica
    r'\sansmath'                # actually tell tex to use it!
    r'\usepackage{siunitx}',    # micro symbols
    r'\sisetup{detect-all}',    # force siunitx to use the fonts
]  


Ne= 63**2
Ni= 32**2

a_rec  = 0.25
re_nrows, re_ncols = 63,63
ri_nrows, ri_ncols = 32,32

Kee = 200
Kei = 200
Kie = 50
Kii = 50


def get_rcr_targets(Nsrc, src_nrows, Ntar, tar_nrows, K):
    sx = np.repeat((np.arange(Nsrc) % src_nrows)/float(src_nrows), K)
    tar_x = (sx + np.random.normal(0, a_rec, size=Nsrc*K)) % 1
    sy = np.repeat((np.arange(Nsrc) / src_nrows)/float(src_nrows), K)
    tar_y = (sy + np.random.normal(0, a_rec, size=Nsrc*K)) % 1
    
    ids = (tar_nrows-1)*np.rint(tar_nrows*tar_x).astype(int) \
          + np.rint((tar_nrows-1)*tar_y).astype(int)
    
    return sx, tar_x, sy, tar_y, ids

sx, tar_x, sy, tar_y, ids = get_rcr_targets(Ne, re_nrows, Ne, re_nrows, 1)

assert(len(tar_x)==len(tar_y))
#pl.plot(sx, sy, '.')
pl.plot(tar_x, tar_y, '.')





pl.tight_layout()
pl.savefig('test1.png', dpi=300)


