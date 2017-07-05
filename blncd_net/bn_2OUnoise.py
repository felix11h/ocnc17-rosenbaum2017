
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
print "(N = {:d})".format(N)
m_e = (N)**0.5*0.015*mV
m_i = (N)**0.5*0.010*mV

method = 'rk2' # 'euler', 'rk4'
T = 20000*ms

model='''
tau  : second (constant)
m    : volt   (constant)
DelT : volt   (constant)

dV/dt = 1/tau*(E_L-V) + 1/tau*DelT*exp((V-V_T)/DelT) + 1/ms*(m+Iex) + 1/tau*Ie_syn + 1/tau*Ii_syn: volt (unless refractory)

Iex : volt (linked)

dIe_syn/dt = -1/tau_syn_e * Ie_syn : volt
dIi_syn/dt = -1/tau_syn_i * Ii_syn : volt

ref : second (constant)
'''

noise_model='''
dIex/dt = -theta*Iex + sigma * xi: volt
'''

Iex1 = NeuronGroup(1, noise_model, method='euler')
Iex2 = NeuronGroup(1, noise_model, method='euler')


# make this one NGrp
NErcr = NeuronGroup(Ne, model, method=method,
                    threshold='V > V_th', reset='V = V_re',
                    refractory='ref')
NIrcr = NeuronGroup(Ni, model, method=method,
                    threshold='V > V_th', reset='V = V_re',
                    refractory='ref')

NErcr.Iex = linked_var(Iex1,'Iex')
NIrcr.Iex = linked_var(Iex2,'Iex')

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

Erec  = StateMonitor(NErcr, ['V','Iex', 'Ie_syn', 'Ii_syn'],
                      record=[0,int(Ne/4), int(Ne/3)])
Irec  = StateMonitor(NErcr, ['V','Iex', 'Ie_syn', 'Ii_syn'],
                      record=[0,int(Ne/4), int(Ne/3)])
ESPKrec = SpikeMonitor(NErcr)
ISPKrec = SpikeMonitor(NIrcr)


NErcr.V = V_re
NIrcr.V = V_re
run(T, report='text')


import os, pickle
pyname = os.path.splitext(os.path.basename(__file__))[0]

fname = "{:s}_N{:d}_T{:d}ms_NS1".format(pyname, N, int(T/ms)) 

with open("data/"+fname+".p", "wb") as pfile:
    pickle.dump(Erec.get_states(),pfile)
    pickle.dump(Irec.get_states(),pfile)
    pickle.dump(ESPKrec.get_states(), pfile)
    pickle.dump(ISPKrec.get_states(), pfile)

