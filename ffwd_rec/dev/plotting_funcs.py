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
plot_raster(ESPKrec.i[(ESPKrec.t>19500*ms)&(ESPKrec.t<20000*ms)],
            ESPKrec.t[(ESPKrec.t>19500*ms)&(ESPKrec.t<20000*ms)],
            marker=',')

pl.savefig('raster_espk.png')

pl.clf()
plot_raster(ISPKrec.i[(ISPKrec.t>19500*ms)&(ISPKrec.t<20000*ms)],
            ISPKrec.t[(ISPKrec.t>19500*ms)&(ISPKrec.t<20000*ms)],
            marker=',')
pl.savefig('raster_ispk.png')



# from brian2tools import 
# pl.clf()
# pl.figure()
# x = brian_plot(ESPKrec[)
# pl.savefig("{}_ESPK.png".format(fname))
# pl.clf()
# x = brian_plot(ISPKrec)
# pl.savefig("{}_ISPK.png".format(fname))
