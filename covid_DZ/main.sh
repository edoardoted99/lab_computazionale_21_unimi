#!/bin/bash

# delete the previous filtering output
find serie_temporali/ -mindepth 1 -delete

# suddivide i vari file in serie temporali suddivise
# per regione e provincia, in una directory apposita.

./split_regioni.sh
./split_provincie.sh 
