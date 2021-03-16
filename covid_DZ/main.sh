#!/bin/bash

# 1) creo directory dati se non esiste
mkdir -p dati
# 2) scarico da internet i dati
url_reg="https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv"
url_prov="https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv"
#curl $url_reg > "dati/${url_reg##*/}"
#curl $url_prov > "dati/${url_prov##*/}"
# 3) elimina l'output del run precedente.
find serie_temporali/ -mindepth 1 -delete
# suddivide i vari file in serie temporali suddivise
# per regione e provincia, in una directory apposita.
# 4) creo la directory per i dati processati
out_dir=serie_temporali
mkdir -p $out_dir
# 5) get the index of the column we want to use to 
# split the data.
# Sfrutto il fatto che nel nostro caso colonna regione
# ha la stessa posizione in entrambi i file da processare.
nome_col_regione="denominazione_regione"
nome_col_provincie="denominazione_provincia"

data_prov="dati/${url_prov##*/}"
data_reg="dati/${url_reg##*/}"

index_regione=$(cat ${data_prov} | 
          ./getindex.awk $nome_col_regione)
index_provincie=$(cat ${data_prov} | 
          ./getindex.awk $nome_col_provincie)
# 6) creo una lista delle regioni, e creo le cartelle
# corrispondenti.

regioni=$(awk 'BEGIN{FS=","}NR>1&&NR<25{gsub(/ /,"_",$'${index_regione}'); print $'${index_regione}'}' $data_reg |
      sort | uniq)
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
# 7) infine runno 2 script awk che smistano i dati
./split_provincie.awk ${out_dir} ${index_regione} ${index_provincie} $data_prov
./split_regioni.awk  ${out_dir} ${index_regione} $data_reg

