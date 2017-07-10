
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pl

from brian2 import *

import sys, importlib
params = importlib.import_module(sys.argv[1])
globals().update(params.__dict__)

# put imports abave (as much as possible) into the separate processes ()

# directory argument for multiprocessing: directory=None
set_device('cpp_standalone')

# prefs.codegen.target = 'auto' (default) Order: 1. Weave, 2. Cython 3. Numpy
# Don't use Weave!

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


Ffwd = PoissonGroup(Nf, rf, name='Fwfd')

NErcr = NeuronGroup(Ne, model, method=method,
                    threshold='V > V_th', reset='V = V_re',
                    refractory='ref', name='NErcr')
NIrcr = NeuronGroup(Ni, model, method=method,
                    threshold='V > V_th', reset='V = V_re',
                    refractory='ref', name='NIrcr')


NErcr.x = 'i / re_nrows'
NErcr.y = 'i % re_nrows'

NIrcr.x = 'i / ri_nrows' 
NIrcr.y = 'i % ri_nrows'

NErcr.ref  = ref_e
NIrcr.ref  = ref_i
NErcr.tau  = tau_e
NIrcr.tau  = tau_i
NErcr.DelT = DelT_e
NIrcr.DelT = DelT_i


def get_targets(a, Nsrc, src_nrows, Ntar, tar_nrows, K):
    tar_x = (np.repeat((np.arange(Nsrc) % src_nrows)/float(src_nrows), K)\
             + np.random.normal(0, a, size=Nsrc*K)) % 1
    tar_y = (np.repeat((np.arange(Nsrc) / src_nrows)/float(src_nrows), K)\
             + np.random.normal(0, a, size=Nsrc*K)) % 1
    ids = tar_nrows*((np.rint((tar_nrows)*tar_x)).astype(int) % tar_nrows) + ((np.rint((tar_nrows)*tar_y)).astype(int) % tar_nrows)
    return ids

S_ee = Synapses(NErcr, NErcr, on_pre='Ie_syn_post += j_ee', name='S_ee')
S_ie = Synapses(NErcr, NIrcr, on_pre='Ie_syn_post += j_ie', name='S_ie')
S_ei = Synapses(NIrcr, NErcr, on_pre='Ii_syn_post += j_ei', name='S_ei')
S_ii = Synapses(NIrcr, NIrcr, on_pre='Ii_syn_post += j_ii', name='S_ii')

S_ee.connect(i = np.repeat(np.arange(Ne),Kee),
             j = get_targets(a_rec, Ne, re_nrows, Ne, re_nrows, Kee))
S_ie.connect(i = np.repeat(np.arange(Ne),Kie),
             j = get_targets(a_rec, Ne, re_nrows, Ni, ri_nrows, Kie))
S_ei.connect(i = np.repeat(np.arange(Ni),Kei),
             j = get_targets(a_rec, Ni, ri_nrows, Ne, re_nrows, Kei))
S_ii.connect(i = np.repeat(np.arange(Ni),Kii),
             j = get_targets(a_rec, Ni, ri_nrows, Ni, ri_nrows, Kii))

S_eF = Synapses(Ffwd, NErcr, on_pre='If_syn_post += j_eF')
S_iF = Synapses(Ffwd, NIrcr, on_pre='If_syn_post += j_iF')

S_eF.connect(i = np.repeat(np.arange(Nf),KeF),
             j = get_targets(a_ffwd, Nf, f_nrows, Ne, re_nrows, KeF))
S_iF.connect(i = np.repeat(np.arange(Nf),KiF),
             j = get_targets(a_ffwd, Nf, f_nrows,  Ni, ri_nrows, KiF))


Erec  = StateMonitor(NErcr, ['V', 'Ie_syn', 'Ii_syn', 'If_syn'],
                     record=np.random.choice(np.arange(Ne), 100, replace=False))
Irec  = StateMonitor(NIrcr, ['V', 'Ie_syn', 'Ii_syn', 'If_syn'],
                     record=np.random.choice(np.arange(Ni), 100, replace=False))

ESPKrec = SpikeMonitor(NErcr, name='ESPKrec')
ISPKrec = SpikeMonitor(NIrcr, name='ISPKrec')
FSPKrec = SpikeMonitor(Ffwd,  name='FSPKrec')

NErcr.V = np.random.uniform(V_re, V_th, size=Ne)*mV
NIrcr.V = np.random.uniform(V_re, V_th, size=Ni)*mV
run(T, report='text')


# netw_state = magic_network.get_states()  # too large
# improvement: can pass argument to get_states
state = {# 'NErcr' : {k:NErcr.get_states()[k] for k in ['x','y']},
         # 'NIrcr' : {k:NIrcr.get_states()[k] for k in ['x','y']},
         # 'S_ee'  : {'j' : S_ee.get_states()['j']},
         # 'S_ie'  : {'j' : S_ie.get_states()['j']},
         # 'S_ei'  : {'j' : S_ei.get_states()['j']},
         # 'S_ii'  : {'j' : S_ii.get_states()['j']},
         # 'S_eF'  : {'j' : S_eF.get_states()['j']},
         # 'S_iF'  : {'j' : S_iF.get_states()['j']},
         'Erec'  : Erec.get_states(),
         'Irec'  : Irec.get_states(),
         # 'ESPK'  : ESPKrec.get_states(),
         # 'ISPK'  : ISPKrec.get_states(),
         # 'FSPK'  : FSPKrec.get_states()
}

import cPickle as pickle
import os
pyname = os.path.splitext(os.path.basename(__file__))[0]

fname = "{:s}_arec{:.2f}_N{:d}_T{:d}ms_Vonly".format(param_set, a_rec, N, int(T/ms)) 

with open("data/"+fname+".p", "wb") as pfile:
    pickle.dump(state, pfile) 
    # pickle.dump(Rrec.get_states(),pfile)
    # pickle.dump(ESPKrec.get_states(), pfile)
    # pickle.dump(ISPKrec.get_states(), pfile)
    # pickle.dump(FSPKrec.get_states(), pfile)

