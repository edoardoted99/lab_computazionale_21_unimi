#!/bin/bash

in_dir=dati-regioni
out_dir=serie_temporali

mkdir -p $out_dir

#1) get the index of the column we want to use to split
# the data.
ref_col_name="denominazione_regione"
# test file è un file campione da cui estrarre
# l'indice associato al campo che ci serve.
test_file=$in_dir/`ls ${in_dir} | head -n 1`
ref_col_index=$(cat ${test_file} | 
          ./getindex.awk $ref_col_name)
# NB: nel file provincie autonome di trento e bolzano
# contano come due regioni distinte.

#2) create directories to contain the sorted data.
regioni=$(awk 'BEGIN{FS=","; getline;}{gsub(/ /,"_",$'${ref_col_index}'); print $'${ref_col_index}'}' $test_file)

for i in $regioni; do
  mkdir -p $out_dir/$i
done


#3) separo i dati relativi a ogni regione.
for i in `ls ${in_dir}`;
do
  ./split_regioni.awk  ${out_dir} ${ref_col_index} $in_dir/$i
done
# ora splitto i file aggregati nei files
# relativi a serie temporali.





