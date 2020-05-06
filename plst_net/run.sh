#!/bin/sh

# simulate networks

python plst_net.py params.red_arec005_params
python plst_net.py params.red_arec010_affwd015_params
python plst_net.py params.red_arec010_affwd020_params
python plst_net.py params.red_arec025_params
python plst_net.py params.red_arec030_affwd015_params
python plst_net.py params.red_arec050_affwd020_params

# make figures

python syn_wtraces.py 
python weight_distance.py
python raster_arec005-025.py
