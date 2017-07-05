
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

r_rows, r_cols = 50,50
a_rec  =
f_rows, f_cols = 24, 24
a_ffwd = 


Nf = 529
rf = 5*Hz

# http://brian2.readthedocs.io/en/2.0rc/examples/synapses.spatial_connections.html?highlight=spatial

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


Ffwd = PoissonGroup(Nf, rf)

NGrp = NeuronGroup(N, model, method='rk4', # rk2, rk4
                    threshold='V > V_th', reset='V = V_re',
                    refractory='ref')

NGrp.Ih_ex = linked_var(Iext,'Ih_ex')

id_sample= np.zeros(N)
id_sample[np.random.choice(np.arange(N),Ni,replace=False)]=1
id_sample = id_sample.astype(bool)

NErcr = NGrp[id_sample]
NIrcr = NGrp[np.invert(id_sample)]

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


