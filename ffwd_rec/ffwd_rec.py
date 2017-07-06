# http://brian2.readthedocs.io/en/2.0rc/examples/synapses.spatial_connections.html?highlight=spatial

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pl

from brian2 import *

set_device('cpp_standalone')

Ne= 63**2
Ni= 32**2
N = Ne+Ni

tau_e = 15*ms
tau_i = 10*ms
E_L  = -60*mV
V_T  = -50*mV
V_re = -65*mV
V_th = -10*mV

DelT_e = 2*mV 
DelT_i = 0.5*mV

ref_e = 1.5*ms
ref_i = 0.5*ms


tau_syn_e = 8*ms 
tau_syn_i = 4*ms
tau_syn_f = tau_syn_e

j_ee = 40*mV / (N**0.5)
j_ie = 120*mV / (N**0.5)
j_ei = -400*mV / (N**0.5)
j_ii = -400*mV / (N**0.5)
j_eF = 120*mV / (N**0.5)
j_iF = 120*mV / (N**0.5)

a_rec  = 0.25
re_nrows, re_ncols = 63,63
ri_nrows, ri_ncols = 32,32
assert((re_nrows**2==Ne) & (ri_nrows**2==Ni))
Kee = 200
Kei = 200
Kie = 500
Kii = 500

a_ffwd = 0.1
f_nrows, f_ncols = 24, 24

KeF = 1000
KiF = 80

Nf = 529
rf = 5*Hz

method = 'rk2'
#T = 10*ms
T = 10000*ms


model='''
grd_id  : integer (constant)
x      : integer (constant)
y      : integer (constant)

tau  : second (constant)
m    : volt   (constant)
DelT : volt   (constant)

dV/dt = 1/tau*(E_L-V) + 1/tau*DelT*exp((V-V_T)/DelT) + 1/tau*Ie_syn + 1/tau*Ii_syn +1/tau*If_syn: volt (unless refractory)

dIe_syn/dt = -1/tau_syn_e * Ie_syn : volt
dIi_syn/dt = -1/tau_syn_i * Ii_syn : volt
dIf_syn/dt = -1/tau_syn_f * If_syn : volt

ref : second (constant)
'''


Ffwd = PoissonGroup(Nf, rf)

NGrp = NeuronGroup(N, model, method=method,
                    threshold='V > V_th', reset='V = V_re',
                    refractory='ref')

NErcr = NGrp[:Ne]
NIrcr = NGrp[Ne:]

NErcr.x = 'i / re_nrows'
NErcr.y = 'i % re_nrows'

NIrcr.x = '(i-Ne) / ri_nrows'
NIrcr.y = '(i-Ne) % ri_nrows'

NErcr.ref  = ref_e
NIrcr.ref  = ref_i
NErcr.tau  = tau_e
NIrcr.tau  = tau_i
NErcr.DelT = DelT_e
NIrcr.DelT = DelT_i


def get_rcr_targets(Nsrc, src_nrows, Ntar, tar_nrows, K):
    tar_x = (np.repeat((np.arange(Nsrc) % src_nrows)/src_nrows, K)\
             + np.random.normal(0, a_rec, size=Nsrc*K)) % 1
    tar_y = (np.repeat((np.arange(Nsrc) / src_nrows)/src_nrows, K)\
             + np.random.normal(0, a_rec, size=Nsrc*K)) % 1
    ids = (tar_nrows-1)*np.rint(tar_nrows*tar_x).astype(int) \
          + np.rint((tar_nrows-1)*tar_y).astype(int)
    return ids

S_ee = Synapses(NErcr, NErcr, on_pre='Ie_syn_post += j_ee')
S_ie = Synapses(NErcr, NIrcr, on_pre='Ie_syn_post += j_ie')
S_ei = Synapses(NIrcr, NErcr, on_pre='Ii_syn_post += j_ei')
S_ii = Synapses(NIrcr, NIrcr, on_pre='Ii_syn_post += j_ii')

S_ee.connect(i = np.repeat(np.arange(Ne),Kee),
             j = get_rcr_targets(Ne, re_nrows, Ne, re_nrows, Kee))
S_ie.connect(i = np.repeat(np.arange(Ne),Kie),
             j = get_rcr_targets(Ne, re_nrows, Ni, ri_nrows, Kie))
S_ei.connect(i = np.repeat(np.arange(Ni),Kei),
             j = get_rcr_targets(Ni, ri_nrows, Ne, re_nrows, Kei))
S_ii.connect(i = np.repeat(np.arange(Ni),Kii),
             j = get_rcr_targets(Ni, ri_nrows, Ni, ri_nrows, Kii))


def get_ffwd_targets(Ntar, tar_nrows, K):
    tar_x = (np.repeat((np.arange(Nf) % f_nrows)/f_nrows, K)\
             + np.random.normal(0, a_ffwd, size=Nf*K)) % 1
    tar_y = (np.repeat((np.arange(Nf) / f_nrows)/f_nrows, K)\
             + np.random.normal(0, a_ffwd, size=Nf*K)) % 1
    ids = (tar_nrows-1)*np.rint(tar_nrows*tar_x).astype(int) \
          + np.rint((tar_nrows-1)*tar_y).astype(int)
    return ids

S_eF = Synapses(Ffwd, NErcr, on_pre='If_syn_post += j_eF')
S_iF = Synapses(Ffwd, NIrcr, on_pre='If_syn_post += j_iF')

S_eF.connect(i = np.repeat(np.arange(Nf),KeF),
             j = get_ffwd_targets(Ne, re_nrows, KeF))
S_iF.connect(i = np.repeat(np.arange(Nf),KiF),
             j = get_ffwd_targets(Ni, ri_nrows, KiF))


Rrec  = StateMonitor(NGrp, ['V', 'Ie_syn', 'Ii_syn', 'If_syn'],
                      record=[0,Ne])
ESPKrec = SpikeMonitor(NErcr)
ISPKrec = SpikeMonitor(NIrcr)
FSPKrec = SpikeMonitor(Ffwd)

NErcr.V = V_re
NIrcr.V = V_re
run(T, report='text')


import os, pickle
pyname = os.path.splitext(os.path.basename(__file__))[0]

fname = "{:s}_N{:d}_T{:d}ms".format(pyname, N, int(T/ms)) 

with open("data/"+fname+".p", "wb") as pfile:
    pickle.dump(Rrec.get_states(),pfile)
    pickle.dump(ESPKrec.get_states(), pfile)
    pickle.dump(ISPKrec.get_states(), pfile)
    pickle.dump(FSPKrec.get_states(), pfile)

