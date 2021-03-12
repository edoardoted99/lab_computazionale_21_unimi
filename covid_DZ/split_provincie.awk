#!/usr/bin/awk -f
# Questo script va eseguito da script_provincie.awk
# in sostanza riceve un file e smista riga per riga
# nei file corretti, in modo che nei file si ricostruisca
# la serie temporale.

# INPUT PARAMS:
# 1) the name of the outdirectory
# 2) index of the region column 
# 3) index of the province column
@load "filefuncs"
# this allow to use a function to test whether a
# given file exists.

BEGIN{
  FS=","
  if(ARGC<3)
  {
    print "usage: add a out_dir name the region and province index"
    exit
  }  
  basepath=ARGV[1]
  reg_n=ARGV[2]
  col_n=ARGV[3]
  ARGV[1]="" 
  ARGV[2]=""
  ARGV[3]="" 
# una particolarità di awk è che di default interpreta
# il primo parametro non nullo come input file, in
# questo è un trick per aggirare (sicuramente ci sono
# modi più furbi).
  getline;
  header = $0
}

{
# rimpiazzo gli spazi nei nomi di regioni/provincie
# con underscore, e rimuovo front slash.
  gsub(/ /,"_",$reg_n)
  gsub(/ /,"_",$col_n)
# this is needed for the strange field fuori regione.
  gsub("/","",$col_n)
# se il file non esiste già lo creo.
  ret=stat(basepath"/"$reg_n"/"$col_n".dat",fdata)
# fdata non so cosa sia, ma se non lo metto 
# non funziona
# if file already exist ret is zero.
  if(ret<0)
  {
# se il file non esiste già, lo creo e gli metto
# l'header dello stesso file in ingresso.
     print header > (basepath"/"$reg_n"/"$col_n".dat")
  }
# riga per riga smisto il contenuto nelle varie
# directory.p
  print >> (basepath"/"$reg_n"/"$col_n".dat")
}
