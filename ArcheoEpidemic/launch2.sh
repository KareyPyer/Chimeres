#!/bin/bash
python ArcheoEpidemic_Chimera4b1.py \
  --seed 42 \
  --steps 500 \
  --pop-total 1000 \
  --nb-zones 8 \
  --root-theme rituel \
  --r0-base 3.0 \
  --mutation-prob 0.05 \
  --random-event-prob 0.08 \
  --log-file logs/chimera_debug.log \
  --log-level DEBUG \
  --export-json ./output \
  --export-network output/network.png \
  --export-csv ./data_knime \
  --export-neo4j ./data_neo4j \
  --verbose
