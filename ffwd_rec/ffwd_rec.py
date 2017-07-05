# http://brian2.readthedocs.io/en/2.0rc/examples/synapses.spatial_connections.html?highlight=spatial

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pl

from brian2 import *

set_device('cpp_standalone')

Ne= 2000
Ni= 500
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

c = 0.25
tau_syn_e = 8*ms 
tau_syn_i = 4*ms
j_ee = 12.5*mV / (N**0.5)
j_ie = 20*mV / (N**0.5)
j_ei = -50*mV / (N**0.5)
j_ii = -50*mV / (N**0.5)

r_nrows, r_ncols = 50,50
a_rec  = 0.25*r_nrows
f_rows, f_cols = 24, 24
a_ffwd = None

Nf = 529
rf = 5*Hz

method = 'rk2'
T = 10*ms
#T = 20000*ms


model='''
grd_id  : integer (constant)
x      : integer (constant)
y      : integer (constant)

tau  : second (constant)
m    : volt   (constant)
DelT : volt   (constant)

dV/dt = 1/tau*(E_L-V) + 1/tau*DelT*exp((V-V_T)/DelT) + 1/tau*Ie_syn + 1/tau*Ii_syn: volt (unless refractory)

dIe_syn/dt = -1/tau_syn_e * Ie_syn : volt
dIi_syn/dt = -1/tau_syn_i * Ii_syn : volt

ref : second (constant)
'''


Ffwd = PoissonGroup(Nf, rf)

NGrp = NeuronGroup(N, model, method=method,
                    threshold='V > V_th', reset='V = V_re',
                    refractory='ref')


# id_sample= np.zeros(N).astype(bool)
# id_sample[np.random.choice(np.arange(N),Ni,replace=False)]=True


# assert(len(NErcr)==Ne)
# assert(len(NIrcr)==Ni)

rnd_ids = np.arange(N) 
np.random.shuffle(rnd_ids)
NGrp.grd_id = rnd_ids

NGrp.x = 'grd_id / r_nrows'
NGrp.y = 'grd_id % r_nrows'

NErcr = NGrp[:Ne]
NIrcr = NGrp[Ne:]

NErcr.ref  = ref_e
NIrcr.ref  = ref_i
NErcr.tau  = tau_e
NIrcr.tau  = tau_i
NErcr.DelT = DelT_e
NIrcr.DelT = DelT_i

S_ee = Synapses(NErcr, NErcr, on_pre='Ie_syn_post += j_ee')
S_ie = Synapses(NErcr, NIrcr, on_pre='Ie_syn_post += j_ie')
S_ei = Synapses(NIrcr, NErcr, on_pre='Ii_syn_post += j_ei')
S_ii = Synapses(NIrcr, NIrcr, on_pre='Ii_syn_post += j_ii')

t_rx = (rnd_ids[:Ne]/r_nrows + np.random.normal(0, a_rec, size=Ne)) % r_nrows
t_ry = (rnd_ids[:Ne] % r_nrows + np.random.normal(0, a_rec, size=Ne)) % r_nrows

t_ids = r_nrows*np.rint(t_rx).astype(int) + np.rint(t_ry).astype(int)



# create list of connections first and the pass Brian2


Rrec  = StateMonitor(NGrp, ['V', 'Ie_syn', 'Ii_syn'],
                      record=[0,Ne])
ESPKrec = SpikeMonitor(NErcr)
ISPKrec = SpikeMonitor(NIrcr)

NErcr.V = V_re
NIrcr.V = V_re

run(T, report='text')


