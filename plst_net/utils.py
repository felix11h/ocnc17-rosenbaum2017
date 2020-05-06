
import numpy as np
from brian2.units import ms

def get_spks(spk, tmin, tmax, ids):
    ''' from SpikeMonitor.get_states() dictionary extract
    '''

    spk_t  = (spk['t'][((spk['t']>tmin) & (spk['t']<=tmax) & (np.in1d(spk['i'],ids)))]-tmin)/ms

    remap  = -1*np.ones(np.max(ids)+1)
    remap[ids] = np.arange(len(ids))
    spk_id = remap[spk['i'][(spk['t']>tmin) & (spk['t']<=tmax) & (np.in1d(spk['i'],ids))]]

    return spk_t, spk_id
