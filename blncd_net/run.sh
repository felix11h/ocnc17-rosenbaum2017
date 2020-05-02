#!/bin/sh

python bn_1OUnoise.py
cd img
python plot_all.py
cd ../
