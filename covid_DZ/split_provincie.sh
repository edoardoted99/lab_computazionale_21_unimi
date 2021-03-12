#!/bin/bash

# split provincie
in_dir=dati-province
out_dir=serie_temporali

mkdir -p $out_dir

#1) get the index of the column we want to use to split
# the data.
nome_col_regione="denominazione_regione"
nome_col_provincie="denominazione_provincia"
# test file è un file campione da cui estrarre
# l'indice associato al campo che ci serve.
test_file=$in_dir/`ls ${in_dir} | head -n 1`
index_regione=$(cat ${test_file} | 
          ./getindex.awk $nome_col_regione)
index_provincie=$(cat ${test_file} | 
          ./getindex.awk $nome_col_provincie)
# NB: nel file provincie autonome di trento e bolzano
# contano come due regioni distinte.

#2) create directories to contain the sorted data.

# first get a list of region names.
# if the directories already exist nothing happens.

regioni=$(awk 'BEGIN{FS=","; getline;}{gsub(/ /,"_",$'${index_regione}'); print $'${index_regione}'}' $test_file)
#nota: il gsub rimpiazza gli space con underscore
#      per i nomi che userò per le directory. Solo 
#      per gusto personale e per usare il metodo
#      sottostante per la creazione di directory.
#      In effetti rende il programma meno efficiente
#      perchè anche quando dovrò splittare i file 
#      dovrò rifare lo stesso procedimento (sostituzione
#      spaces).

for i in $regioni; do
  mkdir -p $out_dir/$i
done


#3) separo i dati relativi a ogni provincia.
for i in `ls ${in_dir}`;
do
# il quarto argomento è il nome del file da 
# processare, facoltativo, potrei anche passarlo 
# nello STDIN.
  ./split_provincie.awk ${out_dir} ${index_regione} ${index_provincie} $in_dir/$i
done





