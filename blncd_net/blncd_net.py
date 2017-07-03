
import matplotlib
matplotlib.use('Agg')
import pylab as pl

from brian2 import *

set_device('cpp_standalone')

defaultclock.dt = 0.1*ms

Ne = 1000
Ni = 1000
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

sigma = 0.1*mV/(ms**0.5)
theta = 1.*1./ms

c = 0.25
tau_syn_e = 8*ms 
tau_syn_i = 4*ms
j_ee = 12.5*mV / (N**0.5)
j_ie = 20*mV / (N**0.5)
j_ei = -50*mV / (N**0.5)
j_ii = -50*mV / (N**0.5)

print "WARNING: Using (N*10) in the noise scaling."
print "If N =/= 1000, this will cause problems!"
m_e = (N*10)**0.5*0.015*mV
m_i = (N*10)**0.5*0.010*mV

T = 20000*ms

model='''
tau  : second (constant)
m    : volt   (constant)
DelT : volt   (constant)

dV/dt = 1/tau*(E_L-V) + 1/tau*DelT*exp((V-V_T)/DelT) + 1/ms*(m+Ih_ex) + 1/tau*Ie_syn + 1/tau*Ii_syn: volt (unless refractory)

Ih_ex : volt (linked)

dIe_syn/dt = -1/tau_syn_e * Ie_syn : volt
dIi_syn/dt = -1/tau_syn_i * Ii_syn : volt

ref : second (constant)
'''

noise_model='''
dIh_ex/dt = -theta*Ih_ex + sigma * xi: volt
'''

Iext = NeuronGroup(1, noise_model, method='euler')


# make this one NGrp
NGrp = NeuronGroup(N, model, method='rk4', # rk2, rk4
                    threshold='V > V_th', reset='V = V_re',
                    refractory='ref')

NGrp.Ih_ex = linked_var(Iext,'Ih_ex')

NErcr = NGrp[:Ne]
NIrcr = NGrp[Ne:]

NErcr.ref  = ref_e
NIrcr.ref  = ref_i
NErcr.tau  = tau_e
NIrcr.tau  = tau_i
NErcr.DelT = DelT_e
NIrcr.DelT = DelT_i
NErcr.m = m_e
NIrcr.m = m_i

S_ee = Synapses(NErcr, NErcr, on_pre='Ie_syn_post += j_ee')
S_ie = Synapses(NErcr, NIrcr, on_pre='Ie_syn_post += j_ie')
S_ei = Synapses(NIrcr, NErcr, on_pre='Ii_syn_post += j_ei')
S_ii = Synapses(NIrcr, NIrcr, on_pre='Ii_syn_post += j_ii')



def connect_EI(N_target, N_source, c):
    #i=[[k]*int(c*N_target) for k in range(N_source)]
    i = np.repeat(np.arange(N_source), int(c*N_target))    
    j = np.random.randint(0,N_target, int(c*N_target)*N_source)

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


VIrec  = StateMonitor(NGrp, ['V','Ih_ex', 'Ie_syn', 'Ii_syn'],
                      record=[0,Ne+1])
ESPKrec = SpikeMonitor(NErcr)
ISPKrec = SpikeMonitor(NIrcr)


NErcr.V = V_re
NIrcr.V = V_re
run(T, report='text')


# --------------------------------------------------------------

pl.clf()
fig, ax = pl.subplots(2,1)
ax[0].plot(VIrec.t/second,VIrec.V[0]/mV)
for t_spk in ESPKrec.t[ESPKrec.i==0]:
    ax[0].plot([t_spk/second]*2, (-50, -30), color='C0')
ax[1].plot(VIrec.t/second, VIrec.Ie_syn[0]/mV)
ax[1].plot(VIrec.t/second, VIrec.Ii_syn[0]/mV)

import os
fname = os.path.splitext(os.path.basename(__file__))[0]
pl.savefig("{}_espk.png".format(fname), dpi=300, bbox_inches='tight')


pl.clf()
fig, ax = pl.subplots(2,1)
ax[0].plot(VIrec.t/second,VIrec[Ne+1].V/mV)
for t_spk in ISPKrec.t[ISPKrec.i==1]:
    ax[0].plot([t_spk/second]*2, (-50, -30), color='C0')
ax[1].plot(VIrec.t/second, VIrec[Ne+1].Ie_syn/mV)
ax[1].plot(VIrec.t/second, VIrec[Ne+1].Ii_syn/mV)

import os
fname = os.path.splitext(os.path.basename(__file__))[0]
pl.savefig("{}_ispk.png".format(fname), dpi=300, bbox_inches='tight')


from brian2tools import plot_raster
pl.clf()
plot_raster(ESPKrec.i, ESPKrec.t, marker=',')
pl.savefig('raster_espk.png')

pl.clf()
plot_raster(ISPKrec.i, ISPKrec.t, marker=',')
pl.savefig('raster_ispk.png')



# from brian2tools import 
# pl.clf()
# pl.figure()
# x = brian_plot(ESPKrec[)
# pl.savefig("{}_ESPK.png".format(fname))
# pl.clf()
# x = brian_plot(ISPKrec)
# pl.savefig("{}_ISPK.png".format(fname))
