#!/usr/bin/awk -f

# - first argument is the name of the outdirectory
# - the second argument is 
@load "filefuncs"
BEGIN{
  FS=OFS=","
  if(ARGC<3)
  {
    print "usage: add a out_dir name a column index."
    exit
  }  
  basepath=ARGV[1]
  col_n=ARGV[2]
  ARGV[1]="" 
  ARGV[2]="" 
  getline;
  header = $0
}
{
# check if region file does exist.
# if it doesn't create it and add a header.
  gsub(/ /,"_",$col_n)
  ret=stat(basepath"/"$col_n"/regione.csv",fdata)
# if file already exist zero is returned.
  if(ret<0)
  {
     print header > (basepath"/"$col_n"/regione.csv")
  }
# write the current line on the correct file.
  print >> (basepath"/"$col_n"/regione.csv")
}
