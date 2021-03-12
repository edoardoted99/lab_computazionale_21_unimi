#!/usr/bin/awk -f

# questo script prende in ingresso un file e una 
# keyword e ritorna l'indice della colonna che 
# corrisponde a tale keyword.
# O stampa un errore sullo standard output.

BEGIN{
  FS=","
  # è pensato per .csv
  if(ARGC==1)
  {
    print "usage: add a field name as argument."
    exit
  }  
  ref=ARGV[1]
  # awk treat the first argument as input file
  # if given, but since we want to use it just 
  # for other purposes we just reset it before.
  # calling getline.
  ARGV[1]="" 
  getline;
  
  for(i=1; i<NF; ++i)
  {
    if($i==ref)
    {
      print i
      exit
    }    
  }
  print "error: field " ref " is missing in the header" > "/dev/fd/2"
}
