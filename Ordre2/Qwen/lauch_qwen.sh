#!/bin/bash
python QweN.py \
    --seed 8888 \
    --steps 50 \
    --pop-total 150 \
    --root-theme rituel \
    --r0-base 2.4 \
    --mutation-prob 0.04 \
    --symbolic-generations 4 \
    --symbolic-pop 8 \
    --export-csv ./output/festin_csv \
    --export-neo4j ./output/festin_neo4j \
    --diffusion-prompt \
    --diffusion-target grok
