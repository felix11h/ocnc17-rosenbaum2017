#!/bin/sh

# simulate

python ffwd_rec.py params.rb_arec005_params
python ffwd_rec.py params.rb_arec025_params

python ffwd_rec.py params.red_arec005_params
python ffwd_rec.py params.red_arec025_params


# make graphics

python syn_currents.py large

python plot_all.py  large
python connectivity_compare.py 
python membrane_potential.py large

python plot_connectivity.py 
python raster_arec005-025.py large


