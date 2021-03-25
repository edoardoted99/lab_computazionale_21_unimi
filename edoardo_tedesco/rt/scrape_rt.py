import pandas as pd #pip3 install pandas
import os

import collections

from datetime import datetime, timedelta
import numpy as np #pip3 install 
import datetime
from io import StringIO
import re
import requests #pip3 install requests
import urllib.request
from pathlib import Path
from tika import parser # pip3 install tika
import pathlib

def download_file(download_url, filename):
        response = urllib.request.urlopen(download_url)    
        file = open(filename + ".pdf", 'wb')
        file.write(response.read())
        file.close()

def to_integer(dt_time):
    return 10000*dt_time.year + 100*dt_time.month + dt_time.day

############### SCRAPE 1 ################

regioni_url = ['Abruzzo', 'Basilicata', 'Calabria' ,'Campania' ,'Emilia-Romagna',
 'Friuli-Venezia-Giulia', 'Lazio', 'Liguria', 'Lombardia' ,'Marche' ,'Molise',
 'Piemonte', 'Puglia', 'Sardegna', 'Sicilia' ,'Toscana' ,'Umbria',
 'ValledAosta', 'Veneto']


base = datetime.date.today()
days = []
date_list = [base - datetime.timedelta(days=x) for x in range(150)]
for day in date_list:
    days.append(to_integer(day))


for regione in regioni_url:
    for data in days:
        url = 'http://www.salute.gov.it/portale/news/documenti/Epi_aggiornamenti/Epi_aggiornamento_'+regione+'_'+str(data)+'.pdf'
        print(url)
        r = requests.get(url, stream=True)
        print(r)
        pdf_path = regione+'/'

        if r.status_code == 200:
            print ('OK!')
           
            Path(str(pathlib.Path().absolute())+"/scrape/"+regione).mkdir(parents=True, exist_ok=True)
            download_file(url, "scrape/"+regione+'/'+regione+'_'+str(data))
        else:
            print ('No Data')


scrape = []

for regione in regioni_url:
    for data in days:
        try:
            relative_path = "/scrape/"+regione+'/'+regione+'_'+str(data)
            path = str(pathlib.Path().absolute())+relative_path
            
            raw = parser.from_file(path+'.pdf')
            text=raw['content']
            try:
                found_rt = re.search('- Rt: (.+?)CI:', text).group(1)
                rt = float(str(found_rt[:-2]))
                s_data = str(data-3)
                s_data = datetime.datetime.strptime(s_data, '%Y%m%d').date()
                scrape.append({"nome_regione": regione, "Rt": rt, "data": s_data})
                
                
            except AttributeError:
                pass
        except:
            pass
        
       
    
print(scrape)

############### SCRAPE2 ##################

c = 0
for j in range(17,49):
    for k in range(1,20):
        
        url = 'http://www.salute.gov.it/imgs/C_17_monitoraggi_'+str(j)+'_'+str(k)+'_fileRegionale.pdf'
        print(url)
        r = requests.get(url, stream=True)
        print(r)
        
        #pdf_path = regione+'/'

        if r.status_code == 200:
            print ('OK!')
            c = c+1
            Path(str(pathlib.Path().absolute())+"/scrape2/").mkdir(parents=True, exist_ok=True)
            path = str(pathlib.Path().absolute())+"/scrape2/"
            download_file(url,path+str(c))
            
        else:
            print ('No Data')

regioni_url2 = ['Abruzzo', 'Basilicata', 'Calabria' ,'Campania' ,'Emilia-Romagna',
 'Friuli-Venezia Giulia', 'Lazio', 'Liguria', 'Lombardia' ,'Marche' ,'Molise',
 'Piemonte', 'Puglia', 'Sardegna', 'Sicilia' ,'Toscana' ,'Umbria',
 "Valle d'Aosta", 'Veneto']


scrape2 = []
errori = []

for c in range(1,551):
    print(c)
    for regione in regioni_url2:
        raw = parser.from_file(str(pathlib.Path().absolute())+"/scrape2/"+str(c)+'.pdf')
        #print(str(c)+'.pdf')
        text=raw['content']
        if re.search(regione, str(text)):
            try:
                
                found_rt = re.search(r'Rt: (.+?) \(', text).group(1)
                found_date = re.findall(r'-(.+?)\n\(', text)
                rt = float(str(found_rt))
                data = datetime.datetime.strptime(str(found_date[0]).replace(" ", ""), '%d/%m/%Y' ).date()
                scrape2.append({"nome_regione": regione, "Rt": rt, "data": data})
                
            except:
                errori.append({"nome_regione": regione,  "data": found_date, "file": str(c)+'.pdf'})
           

############ OUTPUT ##############
csv_columns = ['nome_regione','Rt','data']

import csv


dict_rt = scrape+scrape2
print('scrape', scrape)
print()
print('scrape2', scrape2)
new_dict = []

for el in dict_rt:

    if el['nome_regione']=="Friuli-Venezia-Giulia":
        el['nome_regione']="Friuli Venezia Giulia"
    if el['nome_regione']=="Friuli-Venezia Giulia":
        el['nome_regione']="Friuli Venezia Giulia"

    new_dict.append(el)

csv_file = "scrape.csv"
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in new_dict:
            writer.writerow(data)
except IOError:
    print("I/O error")


import pandas as pd
df=pd.read_csv('scrape.csv')
print(df)
            