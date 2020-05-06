
from brian2.units import *

param_set = 'red'

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


tau_syn_e = 6*ms 
tau_syn_i = 5*ms
tau_syn_f = tau_syn_e

j_ee = 40*mV / (N**0.5)
j_ie = 120*mV / (N**0.5)
j_ei = -400*mV / (N**0.5)
j_ii = -400*mV / (N**0.5)
j_eF = 120*mV / (N**0.5)
j_iF = 120*mV / (N**0.5)

Aplus = 15*mV / (N**0.5)
Aminus = -7.5*mV / (N**0.5)
Wpre_tau = 15*ms
Wpost_tau = 30*ms

a_rec  = 0.10
re_nrows, re_ncols = 63,63
ri_nrows, ri_ncols = 32,32
assert((re_nrows**2==Ne) & (ri_nrows**2==Ni))
Kee = 200
Kei = 200
Kie = 50
Kii = 50

Wee_total = Kee*j_ee

a_ffwd = 0.2
f_nrows, f_ncols = 24, 24

KeF = 1000
KiF = 80

Nf = 576
assert(f_nrows**2==Nf)
rf = 5*Hz

method = 'rk2'
#T = 1*ms#0000*ms
T = 50000*ms
