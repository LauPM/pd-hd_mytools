#!/bin/bash

for i in {1..100}
do
   python3 ../../../iv_curves_pdii/scripts/readV.py >> readV_stability.txt
done