
import matplotlib
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


def make_figures(fname):

    with open('data/'+fname, 'rb') as pfile:
        Erec = pickle.load(pfile)
        Irec = pickle.load(pfile)
        espk = pickle.load(pfile)
        ispk = pickle.load(pfile)


    fig,ax = pl.subplots(2,1)
    fig.set_size_inches(5,5.5)

    Ts = 19500*ms
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



    fig.tight_layout(h_pad=3.25)
    fig.savefig('img/'+fname[3:11]+'_traces.png', dpi=300) 




    fig, ax = pl.subplots(2,1)
    fig.set_size_inches(6,5.5)

    iN = 400
    tmin = 19000*ms
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

    tmin = 19900*ms

    ax[1].plot((Erec['t'][Erec['t']>tmin]-tmin)/ms,
               Erec['Iex'][Erec['t']>tmin]/mV,
               color='blue')
    ax[1].plot((Irec['t'][Irec['t']>tmin]-tmin)/ms,
               Irec['Iex'][Irec['t']>tmin]/mV,
               color='red')

    ax[1].set_xlabel('t [ms]')
    ax[1].set_ylabel('external input [mV]')

    fig.tight_layout()
    fig.savefig('img/'+fname[3:11]+'_raster.png', dpi=300)


fname = 'bn_1OUnoise_N2000_T20000ms_NS1.p'
make_figures(fname)    
fname = 'bn_2OUnoise_N2000_T20000ms_NS1.p'
make_figures(fname)
