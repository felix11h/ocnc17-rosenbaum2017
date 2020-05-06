from brian2.units import mV,ms
import cPickle as pickle
import pylab as pl
import numpy as np

with open('../data/plst_net_red_arec0.05_N4993_T50000ms_scaling.p', 'rb') as pfile:
    states005 = pickle.load(pfile)
# with open('../data/plst_net_red_arec0.25_N4993_T50000ms_scaling.p', 'rb') as pfile:
#     states025 = pickle.load(pfile)


# with open('../data/plst_net_red_arec0.05_N4993_T50000ms_stdphom_selfrm.p', 'rb') as pfile:
#     states005 = pickle.load(pfile)
# with open('../data/plst_net_red_arec0.25_N4993_T50000ms_stdphom_selfrm.p', 'rb') as pfile:
#     states025 = pickle.load(pfile)

# with open('../data/plst_net_red_arec0.10_affwd0.20_N4993_T50000ms_stdphom_selfrm.p', 'rb') as pfile:
#     states010 = pickle.load(pfile)
# with open('../data/plst_net_red_arec0.50_affwd0.20_N4993_T50000ms_stdphom_selfrm.p', 'rb') as pfile:
#     states050 = pickle.load(pfile)



states = states005
    
x = states['S_ee']['w']
pl.hist(x/mV, 50)
pl.savefig('new.png', dpi=300)

t = states['SEERec']['t']
ws = states['SEERec']['w']

pl.clf()
for k in range(5):
    pl.plot(t/ms, ws[:,k]/mV)

pl.savefig('new2.png', dpi=300)


states=states005
NE=states['NErcr']
See = states['S_ee']

dists = [np.sqrt((abs(NE['x'][See['i'][k]] - NE['x'][See['j'][k]]) % 32)**2 + (abs(NE['y'][See['i'][k]] - NE['y'][See['j'][k]]) % 32)**2) for k in range(len(See['i']))]

n, dbins = np.histogram(dists, bins=50)
sy, _  = np.histogram(dists, bins=dbins, weights=See['w'])
sy2, _  = np.histogram(dists, bins=dbins, weights=See['w']*See['w'])

centers = 0.5*(dbins[1:]+dbins[:-1])

pl.plot(centers, sy/n, label='a_rec = 0.05, a_ffwd = 0.10', linewidth=3.)

# states=states025
# NE=states['NErcr']
# See = states['S_ee']

# dists = [np.sqrt((abs(NE['x'][See['i'][k]] - NE['x'][See['j'][k]]) % 32)**2 + (abs(NE['y'][See['i'][k]] - NE['y'][See['j'][k]]) % 32)**2) for k in range(len(See['i']))]

# n, dbins = np.histogram(dists, bins=50)
# sy, _  = np.histogram(dists, bins=dbins, weights=See['w'])
# sy2, _  = np.histogram(dists, bins=dbins, weights=See['w']*See['w'])

# centers = 0.5*(dbins[1:]+dbins[:-1])

# pl.plot(centers, sy/n, '.')

# states=states010
# NE=states['NErcr']
# See = states['S_ee']

# dists = [np.sqrt((abs(NE['x'][See['i'][k]] - NE['x'][See['j'][k]]) % 32)**2 + (abs(NE['y'][See['i'][k]] - NE['y'][See['j'][k]]) % 32)**2) for k in range(len(See['i']))]

# n, dbins = np.histogram(dists, bins=50)
# sy, _  = np.histogram(dists, bins=dbins, weights=See['w'])
# sy2, _  = np.histogram(dists, bins=dbins, weights=See['w']*See['w'])

# centers = 0.5*(dbins[1:]+dbins[:-1])

# pl.plot(centers, sy/n, '.')

# states=states050
# NE=states['NErcr']
# See = states['S_ee']

# dists = [np.sqrt((abs(NE['x'][See['i'][k]] - NE['x'][See['j'][k]]) % 32)**2 + (abs(NE['y'][See['i'][k]] - NE['y'][See['j'][k]]) % 32)**2) for k in range(len(See['i']))]

# n, dbins = np.histogram(dists, bins=50)
# sy, _  = np.histogram(dists, bins=dbins, weights=See['w'])
# sy2, _  = np.histogram(dists, bins=dbins, weights=See['w']*See['w'])

# centers = 0.5*(dbins[1:]+dbins[:-1])

# pl.plot(centers, sy/n, '.')



# pl.legend(loc='upper right', framealpha=1., frameon=False)

# pl.savefig('scatter.png', dpi=300)
