#!/bin/bash
python Kimi.py --seed 1989 --verbose --steps 400  --pop-total 400 --export-csv ./out_csv --export-neo4j ./out_neo4j --export-collage ./collage.png --diffusion-prompt ./prompt.txt --diffusion-target gemini 
