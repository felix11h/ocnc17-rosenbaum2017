
from brian2 import *

set_device('cpp_standalone')

seed(1234)
np.random.seed(1234)

defaultclock.dt = 0.1*ms

Ne, Ni = 10000, 10000
N = Ne+Ni

tau_e, tau_i = 15*ms, 10*ms

E_L  = -60*mV
V_T  = -50*mV
V_re = -65*mV
V_th = -10*mV

DelT_e, DelT_i = 2*mV, 0.5*mV
ref_e, ref_i = 1.5*ms, 0.5*ms

sigma = 0.1*mV/(ms**0.5)
theta = 1.*1./ms

c = 0.25
tau_syn_e = 8*ms 
tau_syn_i = 4*ms
j_ee = 12.5*mV / (N**0.5)
j_ie = 20*mV / (N**0.5)
j_ei = -50*mV / (N**0.5)
j_ii = -50*mV / (N**0.5)

print("WARNING: Using (N*10) in the noise scaling.")
print("If N =/= 1000, this will cause problems!")
print("(N = {:d})".format(N))

m_e = (N)**0.5*0.015*mV
m_i = (N)**0.5*0.010*mV

method = 'rk2' # 'euler', 'rk4'
T = 20000*ms

model='''
      tau  : second (constant)
      m    : volt   (constant)
      DelT : volt   (constant)

      dV/dt = 1/tau*(E_L-V) + 1/tau*DelT*exp((V-V_T)/DelT) 
              + 1/ms*(m+Iex) + 1/tau*Ie_syn 
              + 1/tau*Ii_syn: volt (unless refractory)

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
NErcr1 = NeuronGroup(Ne/2, model, method=method,
                    threshold='V > V_th', reset='V = V_re',
                    refractory='ref')
NErcr2 = NeuronGroup(Ne/2, model, method=method,
                    threshold='V > V_th', reset='V = V_re',
                    refractory='ref')

NIrcr1 = NeuronGroup(Ni/2, model, method=method,
                    threshold='V > V_th', reset='V = V_re',
                    refractory='ref')
NIrcr2 = NeuronGroup(Ni/2, model, method=method,
                    threshold='V > V_th', reset='V = V_re',
                    refractory='ref')


NErcr1.Iex = linked_var(Iex1,'Iex')
NIrcr1.Iex = linked_var(Iex1,'Iex')
NErcr2.Iex = linked_var(Iex2,'Iex')
NIrcr2.Iex = linked_var(Iex2,'Iex')

for NErcr in [NErcr1, NErcr2]:
    NErcr.ref  = ref_e
    NErcr.tau  = tau_e
    NErcr.DelT = DelT_e
    NErcr.m = m_e
   
for NIrcr in [NIrcr1, NIrcr2]:
    NIrcr.ref  = ref_i
    NIrcr.tau  = tau_i
    NIrcr.DelT = DelT_i
    NIrcr.m = m_i 

S_ee11 = Synapses(NErcr1, NErcr1, on_pre='Ie_syn_post += j_ee')
S_ee22 = Synapses(NErcr2, NErcr2, on_pre='Ie_syn_post += j_ee')
S_ee12 = Synapses(NErcr1, NErcr2, on_pre='Ie_syn_post += j_ee')
S_ee21 = Synapses(NErcr2, NErcr1, on_pre='Ie_syn_post += j_ee')

S_ie11 = Synapses(NErcr1, NIrcr1, on_pre='Ie_syn_post += j_ie')
S_ie22 = Synapses(NErcr2, NIrcr2, on_pre='Ie_syn_post += j_ie')
S_ie12 = Synapses(NErcr1, NIrcr2, on_pre='Ie_syn_post += j_ie')
S_ie21 = Synapses(NErcr2, NIrcr1, on_pre='Ie_syn_post += j_ie')

S_ei11 = Synapses(NIrcr1, NErcr1, on_pre='Ii_syn_post += j_ei')
S_ei22 = Synapses(NIrcr2, NErcr2, on_pre='Ii_syn_post += j_ei')
S_ei12 = Synapses(NIrcr1, NErcr2, on_pre='Ii_syn_post += j_ei')
S_ei21 = Synapses(NIrcr2, NErcr1, on_pre='Ii_syn_post += j_ei')

S_ii11 = Synapses(NIrcr1, NIrcr1, on_pre='Ii_syn_post += j_ii')
S_ii22 = Synapses(NIrcr2, NIrcr2, on_pre='Ii_syn_post += j_ii')
S_ii12 = Synapses(NIrcr1, NIrcr2, on_pre='Ii_syn_post += j_ii')
S_ii21 = Synapses(NIrcr2, NIrcr1, on_pre='Ii_syn_post += j_ii')


def connect_EI(N_target, N_source, c):
    #i=[[k]*int(c*N_target) for k in range(N_source)]
    i = np.repeat(np.arange(N_source), int(c*N_target))    
    j = np.random.randint(0,N_target, int(c*N_target)*N_source)

    assert(len(i) == len(j))
    assert(max(i) == N_source-1)    
    return {'i':i,'j':j}

S_ee11.connect(**connect_EI(int(Ne/2),int(Ne/2),c))
S_ee22.connect(**connect_EI(int(Ne/2),int(Ne/2),c))
S_ee12.connect(**connect_EI(int(Ne/2),int(Ne/2),c))
S_ee21.connect(**connect_EI(int(Ne/2),int(Ne/2),c))

S_ie11.connect(**connect_EI(int(Ni/2),int(Ne/2),c))
S_ie22.connect(**connect_EI(int(Ni/2),int(Ne/2),c))
S_ie12.connect(**connect_EI(int(Ni/2),int(Ne/2),c))
S_ie21.connect(**connect_EI(int(Ni/2),int(Ne/2),c))

S_ei11.connect(**connect_EI(int(Ne/2),int(Ni/2),c))
S_ei22.connect(**connect_EI(int(Ne/2),int(Ni/2),c))
S_ei12.connect(**connect_EI(int(Ne/2),int(Ni/2),c))
S_ei21.connect(**connect_EI(int(Ne/2),int(Ni/2),c))

S_ii11.connect(**connect_EI(int(Ni/2),int(Ni/2),c))
S_ii22.connect(**connect_EI(int(Ni/2),int(Ni/2),c))
S_ii12.connect(**connect_EI(int(Ni/2),int(Ni/2),c))
S_ii21.connect(**connect_EI(int(Ni/2),int(Ni/2),c))


Erec  = StateMonitor(NErcr1, ['V','Iex', 'Ie_syn', 'Ii_syn'],
                     record=[0,int(Ne/4), int(Ne/3)])
Irec  = StateMonitor(NIrcr1, ['V','Iex', 'Ie_syn', 'Ii_syn'],
                     record=[0,int(Ne/4), int(Ne/3)])

ESPKrec = SpikeMonitor(NErcr1)
ISPKrec = SpikeMonitor(NIrcr1)


NErcr1.V, NErcr2.V = V_re, V_re
NIrcr1.V, NIrcr2.V = V_re, V_re

# schedule summary
run(T, report='text')


import os, pickle
pyname = os.path.splitext(os.path.basename(__file__))[0]

fname = "{:s}_N{:d}_T{:d}ms_NS1".format(pyname, N, int(T/ms)) 

with open("data/"+fname+".p", "wb") as pfile:
    pickle.dump(Erec.get_states(),pfile)
    pickle.dump(Irec.get_states(),pfile)
    pickle.dump(ESPKrec.get_states(), pfile)
    pickle.dump(ISPKrec.get_states(), pfile)

