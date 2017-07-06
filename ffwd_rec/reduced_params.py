
from brian2.units import *

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


tau_syn_e = 8*ms 
tau_syn_i = 4*ms
tau_syn_f = tau_syn_e

j_ee = 40*mV / (N**0.5)
j_ie = 120*mV / (N**0.5)
j_ei = -400*mV / (N**0.5)
j_ii = -400*mV / (N**0.5)
j_eF = 120*mV / (N**0.5)
j_iF = 120*mV / (N**0.5)

a_rec  = 0.25
re_nrows, re_ncols = 63,63
ri_nrows, ri_ncols = 32,32
assert((re_nrows**2==Ne) & (ri_nrows**2==Ni))
Kee = 200
Kei = 200
Kie = 50
Kii = 50

a_ffwd = 0.1
f_nrows, f_ncols = 24, 24

KeF = 1000
KiF = 80

Nf = 529
rf = 5*Hz

method = 'rk2'
#T = 10*ms
T = 10000*ms
