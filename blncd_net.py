
import matplotlib
matplotlib.use('Agg')
import pylab as pl

from brian2 import *


Ne = 2500
Ni = 2500
N = Ne+Ni

tau = 10*ms
V_th = -50*mV
E = -60*mV

sigma = 2.5*mV/(ms**0.5)
mu = 9*mV
theta = 1.*1./ms

tau_syn_e = 6*ms 
tau_syn_i = 5*ms
j_ee = 12.5*mV / (N**0.5)
j_ie = 20*mV / (N**0.5)
j_ei = -50*mV / (N**0.5)
j_ii = -50*mV / (N**0.5)

T = 2000*ms

model='''
dV/dt = 1./tau*(E-V) + 1./tau*Ih_ex + 1./tau_syn_e*Ie_syn + 1./tau_syn_i*Ii_syn: volt
Ih_ex : volt (linked)
dIe_syn/dt = -1/tau_syn_e * Ie_syn : volt
dIi_syn/dt = -1/tau_syn_i * Ii_syn : volt
'''

noise_model='''
dIh_ex/dt = theta*(mu-Ih_ex) + sigma * xi: volt
'''

Iext = NeuronGroup(1, noise_model, method='euler')

# tau_ref !!
NErcr = NeuronGroup(Ne, model, method='euler',
                   threshold='V > V_th', reset='V = E')
NIrcr = NeuronGroup(Ni, model, method='euler',
                   threshold='V > V_th', reset='V = E')
NErcr.Ih_ex = linked_var(Iext,'Ih_ex')
NIrcr.Ih_ex = linked_var(Iext,'Ih_ex')


S_ee = Synapses(NErcr, NErcr, on_pre='Ie_syn_post += j_ee')
S_ie = Synapses(NErcr, NIrcr, on_pre='Ie_syn_post += j_ie')
S_ei = Synapses(NIrcr, NErcr, on_pre='Ii_syn_post += j_ei')
S_ii = Synapses(NIrcr, NIrcr, on_pre='Ii_syn_post += j_ii')

c = 0.25
# S_ee.connect(i=range(Ne), j=[np.random.choice(range(Ne),int(c*Ne)) for i in range(Ne)])
# S_ie.connect(i=range(Ne), j=[np.random.choice(range(Ni),int(c*Ni)) for i in range(Ne)])
# S_ei.connect(i=range(Ni), j=[np.random.choice(range(Ne),int(c*Ne)) for i in range(Ni)])
# S_ii.connect(i=range(Ni), j=[np.random.choice(range(Ni),int(c*Ni)) for i in range(Ni)])

S_ee.connect(p=c)
S_ie.connect(p=c)
S_ei.connect(p=c)
S_ii.connect(p=c)  



VIrec  = StateMonitor(NErcr, ['V','Ih_ex', 'Ie_syn', 'Ii_syn'],
                      record=[0])
ESPKrec = SpikeMonitor(NErcr)
ISPKrec = SpikeMonitor(NIrcr)


NErcr.V = E
NIrcr.V = E
run(T)

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
x = brian_plot(ESPKrec)
pl.savefig("{}_ESPK.png".format(fname))
