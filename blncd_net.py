
import matplotlib
matplotlib.use('Agg')
import pylab as pl

from brian2 import *


Ne = 10000
Ni = 10000
N = Ne+Ni

V_th = -50*mV
E = -60*mV
tau_e = 15*ms
tau_i = 10*ms
ref_e = 1.5*ms
ref_i = 0.5*ms

sigma = 2.5*mV/(ms**0.5)
mu = 9*mV
theta = 1.*1./ms

c = 0.25
tau_syn_e = 6*ms 
tau_syn_i = 5*ms
j_ee = 12.5*mV / (N**0.5)
j_ie = 20*mV / (N**0.5)
j_ei = -50*mV / (N**0.5)
j_ii = -50*mV / (N**0.5)

m_e = N**0.5*0.015*mV
m_i = N**0.5*0.010*mV

T = 2000*ms

model='''
tau : second (constant)
m   : volt   (constant)
dV/dt = 1./tau*(E-V) + 1./tau*(m+Ih_ex) + 1./tau_syn_e*Ie_syn + 1./tau_syn_i*Ii_syn: volt

Ih_ex : volt (linked)

dIe_syn/dt = -1/tau_syn_e * Ie_syn : volt
dIi_syn/dt = -1/tau_syn_i * Ii_syn : volt
'''

noise_model='''
dIh_ex/dt = -theta*Ih_ex + sigma * xi: volt
'''

Iext = NeuronGroup(1, noise_model, method='euler')
Iext

NErcr = NeuronGroup(Ne, model, method='euler',
                    threshold='V > V_th', reset='V = E',
                    refractory=ref_e)
NIrcr = NeuronGroup(Ni, model, method='euler',
                    threshold='V > V_th', reset='V = E',
                    refractory=ref_i)

NErcr.Ih_ex = linked_var(Iext,'Ih_ex')
NIrcr.Ih_ex = linked_var(Iext,'Ih_ex')
NErcr.tau = tau_e
NIrcr.tau = tau_i
NErcr.m = m_e
NIrcr.m = m_i

S_ee = Synapses(NErcr, NErcr, on_pre='Ie_syn_post += j_ee')
S_ie = Synapses(NErcr, NIrcr, on_pre='Ie_syn_post += j_ie')
S_ei = Synapses(NIrcr, NErcr, on_pre='Ii_syn_post += j_ei')
S_ii = Synapses(NIrcr, NIrcr, on_pre='Ii_syn_post += j_ii')



def connect_EI(N_target, N_source, c):
    i=[[k]*int(c*N_target) for k in range(N_source)]
    j=[np.random.choice(range(N_target),int(c*N_target)) for k in range(N_source)]
    i, j = np.array(i).flatten(), np.array(j).flatten()
    assert(len(i) == len(j))
    assert(max(i) == N_source-1)    
    return {'i':i,'j':j}

S_ee.connect(**connect_EI(Ne,Ne,c))
S_ie.connect(**connect_EI(Ni,Ne,c))
S_ei.connect(**connect_EI(Ne,Ni,c))
S_ii.connect(**connect_EI(Ni,Ni,c))

# S_ee.connect(p=c)
# S_ie.connect(p=c)
# S_ei.connect(p=c)
# S_ii.connect(p=c)


VIrec  = StateMonitor(NErcr, ['V','Ih_ex', 'Ie_syn', 'Ii_syn'],
                      record=[0])
ESPKrec = SpikeMonitor(NErcr)
ISPKrec = SpikeMonitor(NIrcr)


NErcr.V = E
NIrcr.V = E
run(T)


# --------------------------------------------------------------


fig, ax = pl.subplots(2,1)
ax[0].plot(VIrec.t/second,VIrec.V[0]/mV)
for t_spk in ESPKrec.t[ESPKrec.i==0]:
    ax[0].plot([t_spk/second]*2, (-50, -30), color='C0')
ax[1].plot(VIrec.t/second, VIrec.Ie_syn[0]/mV)
ax[1].plot(VIrec.t/second, VIrec.Ii_syn[0]/mV)

import os
fname = os.path.splitext(os.path.basename(__file__))[0]
pl.savefig("{}.png".format(fname), dpi=300, bbox_inches='tight')

from brian2tools import brian_plot
pl.clf()
pl.figure()
x = brian_plot(ISPKrec)
pl.savefig("{}_ESPK.png".format(fname))
