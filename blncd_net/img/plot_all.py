
import matplotlib
#matplotlib.style.use('classic')
matplotlib.use('Agg')
import matplotlib.pyplot as pl

from brian2.units import *

import pickle

# with open('../data/blncd_net_N2000_T20000ms.p', 'rb') as pfile:
#     vi = pickle.load(pfile)
#     espk = pickle.load(pfile)
#     ispk = pickle.load(pfile)

with open('../data/bn_1OUnoise_N2000_T20000ms_NS1.p', 'rb') as pfile:
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


# fig,ax = pl.subplots(2,1)
# fig.set_size_inches(5,4.)

# Ts = 19500*ms
# k = 3

# ax[0].set_xlabel('t [s]')
# ax[0].set_ylabel('V [mV]')
# ax[0].plot(vi['t'][vi['t']>Ts],
#         vi['V'].T[k][vi['t']>Ts]/mV)
# ax[0].margins(0.01)


# ax[1].set_xlabel('t [s]')
# ax[1].set_ylabel('V [mV]')
# ax[1].plot(vi['t'][vi['t']>Ts],
#            vi['Ie_syn'].T[k][vi['t']>Ts]/mV,
#            label=r'$I^{\text{exc}}_{\text{syn}}$')
# ax[1].plot(vi['t'][vi['t']>Ts],
#            vi['Ii_syn'].T[k][vi['t']>Ts]/mV,
#            label=r'$I^{\text{inh}}_{\text{syn}}$')
# ax[1].plot(vi['t'][vi['t']>Ts],
#            (vi['Ie_syn'].T[k][vi['t']>Ts] + \
#             vi['Ii_syn'].T[k][vi['t']>Ts])/mV,
#            color='gray',
#            label=r'$I^{\text{inh}}_{\text{syn}}' +\
#                  r' + I^{\text{inh}}_{\text{syn}}$')

# ax[1].set_ylim(-60,60)
# ax[1].margins(0.01)

# ax[1].legend(bbox_to_anchor=(0., 1.01, 1., .101),
#              loc='lower center', framealpha=1., ncol=3,
#              frameon=False)



# pl.tight_layout(h_pad=3.25)
# fig.savefig('name.png', dpi=300) #bbox_inches='tight')




fig, ax = pl.subplots()
fig.set_size_inches(6,3)

iN = 400
tmin = 18000*ms

ax.plot(espk['t'][(espk['t']>tmin) & (espk['i']<iN)],
        espk['i'][(espk['t']>tmin) & (espk['i']<iN)],
        '.', color='blue', markersize=.5)
ax.plot(ispk['t'][(ispk['t']>tmin) & (ispk['i']<iN)],
        iN+ispk['i'][(ispk['t']>tmin) & (ispk['i']<iN)],
        '.', color='red', markersize=.5)

ax.margins(0.0)
ax.set_xlabel('t [s]')
ax.set_ylabel('index i')

pl.tight_layout()
fig.savefig('new.png', dpi=300)


