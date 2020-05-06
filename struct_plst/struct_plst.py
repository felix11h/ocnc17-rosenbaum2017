
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pl

from brian2 import *

import sys, importlib
params = importlib.import_module(sys.argv[1])
globals().update(params.__dict__)

set_device('cpp_standalone', directory=None, build_on_run=False)


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

Wsum : volt 
'''

# can't write dP/dt when P is (shared)
# update (shared) at beginning of a clock
syn_model='''
w : volt
dWpre/dt=-Wpre/Wpre_tau : volt (event-driven)
dWpost/dt=-Wpost/Wpost_tau : volt (event-driven)

Wsum_post = w : volt (summed)

active : integer 
P : 1 (shared)
'''

pre_model='''
Ie_syn_post += int(active)*w
Wpre += Aplus
w = clip(w+int(active)*Wpost, 0*mV, 10*mV)
'''

post_model='''
Wpost += Aminus
w = clip(w+int(active)*Wpre, 0*mV, 10*mV) 
'''

regular_model='''
w = w*(Wee_total/Wsum_post)
'''

# rand() == uniform(0,1)
struct_model='''
r = rand()
should_stay_active = (w > pruning_threshold)
should_become_active = (r < P)
was_active_before = active
active = int(active==1) * int(should_stay_active) + int(active==0) * int(should_become_active)'''


print('Weights are not inserted at insertion weight yet! Fix this before doing anything else!')
insertion_mech='''
w = w*was_active_before*active + w_insertion*was_not_active_before*active 
'''

Ffwd = PoissonGroup(Nf, rf, name='Fwfd')

NErcr = NeuronGroup(Ne, model, method=method,
                    threshold='V > V_th', reset='V = V_re',
                    refractory='ref', name='NErcr')
NIrcr = NeuronGroup(Ni, model, method=method,
                    threshold='V > V_th', reset='V = V_re',
                    refractory='ref', name='NIrcr')


NErcr.x = 'i // re_nrows'
NErcr.y = 'i % re_nrows'

NIrcr.x = 'i // ri_nrows' 
NIrcr.y = 'i % ri_nrows'

NErcr.ref  = ref_e
NIrcr.ref  = ref_i
NErcr.tau  = tau_e
NIrcr.tau  = tau_i
NErcr.DelT = DelT_e
NIrcr.DelT = DelT_i


S_ee = Synapses(NErcr, NErcr, model=syn_model, on_pre=pre_model, on_post=post_model, name='S_ee')
S_ee.summed_updaters['Wsum_post']._clock = Clock(dt=10*ms)
S_ee.run_regularly(regular_model, dt = 10*ms, when='end')
S_ee.run_regularly(struct_model, dt = 1*ms, when='end')

S_ie = Synapses(NErcr, NIrcr, on_pre='Ie_syn_post += j_ie', name='S_ie')
S_ei = Synapses(NIrcr, NErcr, on_pre='Ii_syn_post += j_ei', name='S_ei')
S_ii = Synapses(NIrcr, NIrcr, on_pre='Ii_syn_post += j_ii', name='S_ii')

S_ee.connect(p=0.1)
S_ie.connect(p=0.1)
S_ei.connect(p=0.1)
S_ii.connect(p=0.1)    

S_eF = Synapses(Ffwd, NErcr, on_pre='If_syn_post += j_eF')
S_iF = Synapses(Ffwd, NIrcr, on_pre='If_syn_post += j_iF')

S_eF.connect(p=0.1)
S_iF.connect(p=0.1)


S_ee.w = j_ee
S_ee.P = P

Erec  = StateMonitor(NErcr, ['V', 'Ie_syn', 'Ii_syn', 'If_syn'],
                     record=np.random.choice(np.arange(Ne), 1, replace=False))
Irec  = StateMonitor(NIrcr, ['V', 'Ie_syn', 'Ii_syn', 'If_syn'],
                     record=np.random.choice(np.arange(Ni), 1, replace=False))

ESPKrec = SpikeMonitor(NErcr, name='ESPKrec')
ISPKrec = SpikeMonitor(NIrcr, name='ISPKrec')
FSPKrec = SpikeMonitor(Ffwd,  name='FSPKrec')


SEERec = StateMonitor(S_ee, ['w'], record=np.random.choice(np.arange(Ne*Kee-1), 5, replace=False), dt=5*ms)


NErcr.V = np.random.uniform(V_re, V_th, size=Ne)*mV
NIrcr.V = np.random.uniform(V_re, V_th, size=Ni)*mV


# print(scheduling_summary())

run(T, report='text')
device.build(directory=None) #needs directory argument?


state = {# 'NErcr' : NErcr.get_states(['x','y']),
         # 'NIrcr' : NIrcr.get_states(['x','y']),
         # 'SEERec': SEERec.get_states(),
         'S_ee'  : S_ee.get_states(['i','j','w']),
         # 'S_ie'  : {'j' : S_ie.get_states()['j']},
         # 'S_ei'  : {'j' : S_ei.get_states()['j']},
         # 'S_ii'  : {'j' : S_ii.get_states()['j']},
         # 'S_eF'  : {'j' : S_eF.get_states()['j']},
         # 'S_iF'  : {'j' : S_iF.get_states()['j']},
         # 'Erec'  : Erec.get_states(),
         # 'Irec'  : Irec.get_states(),
         # 'ESPK'  : ESPKrec.get_states(),
         # 'ISPK'  : ISPKrec.get_states(),
         # 'FSPK'  : FSPKrec.get_states()
}

import os, pickle
pyname = os.path.splitext(os.path.basename(__file__))[0]

fname = "struct_plst_{:s}_arec{:.2f}_affwd{:.2f}_N{:d}_T{:d}ms_test".format(param_set, a_rec, a_ffwd, N, int(T/ms)) 

with open("data/"+fname+".p", "wb") as pfile:
    pickle.dump(state, pfile) 

