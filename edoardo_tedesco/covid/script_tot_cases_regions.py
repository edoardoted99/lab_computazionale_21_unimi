import sqlite3
from sqlite3 import Error

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.dates as md

import numpy as np
import datetime as dt
import time

import pandas as pd

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        connection.row_factory = lambda cursor, row: row[0]
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

connection = create_connection("covid.db")
c = connection.cursor()

## getting relative path of data.csv
import os
dirname = os.path.dirname(os.path.abspath(__file__))
path_province = r'%s' % dirname + '/csv/dpc-covid19-ita-province.csv'
path_regioni = r'%s' % dirname + '/csv/dpc-covid19-ita-regioni.csv'
##

## reading csv
read_province = pd.read_csv (path_province)
read_regioni = pd.read_csv (path_regioni)

## filling database covid.db
try:
    read_regioni.to_sql('regioni', connection, if_exists='append', index = False) # Insert the values from the csv file into the table 'regioni'
    read_province.to_sql('province', connection, if_exists='append', index = False) # Insert the values from the csv file into the table 'province'
except:
    pass
##

## launch query to get all regions
regioni = c.execute('select distinct denominazione_regione from regioni').fetchall()
print(regioni)
##

## utility for plot style
colours = ["aliceblue","antiquewhite","aqua","aquamarine","azure","beige","bisque","black","blanchedalmond","blue","blueviolet","brown","burlywood","cadetblue","chartreuse","chocolate","coral","cornflowerblue","cornsilk","crimson","cyan","darkblue","darkcyan","darkgoldenrod","darkgray","darkgrey","darkgreen","darkkhaki","darkmagenta","darkolivegreen","darkorange","darkorchid","darkred","darksalmon","darkseagreen","darkslateblue","darkslategray","darkslategrey","darkturquoise","darkviolet","deeppink","deepskyblue","dimgray","dimgrey","dodgerblue","firebrick","floralwhite","forestgreen","fuchsia","gainsboro","ghostwhite","gold","goldenrod","gray","grey","green","greenyellow","honeydew","hotpink","indianred","indigo","ivory","khaki","lavender","lavenderblush","lawngreen","lemonchiffon","lightblue","lightcoral","lightcyan","lightgoldenrodyellow","lightgray","lightgrey","lightgreen","lightpink","lightsalmon","lightseagreen","lightskyblue","lightslategray","lightslategrey","lightsteelblue","lightyellow","lime","limegreen","linen","magenta","maroon","mediumaquamarine","mediumblue","mediumorchid","mediumpurple","mediumseagreen","mediumslateblue","mediumspringgreen","mediumturquoise","mediumvioletred","midnightblue","mintcream","mistyrose","moccasin","navajowhite","navy","oldlace","olive","olivedrab","orange","orangered","orchid","palegoldenrod","palegreen","paleturquoise","palevioletred","papayawhip","peachpuff","peru","pink","plum","powderblue","purple","rebeccapurple","red","rosybrown","royalblue","saddlebrown","salmon","sandybrown","seagreen","seashell","sienna","silver","skyblue","slateblue","slategray","slategrey","snow","springgreen","steelblue","tan","teal","thistle","tomato","turquoise","violet","wheat","white","whitesmoke","yellow","yellowgreen"]
i=0
patches = []
##


for regione in regioni:
    ##query to get all id_data
    s = 'select id from regioni where denominazione_regione="'+regione+'";' 
    ids_data = c.execute(s).fetchall()
    ##
    
    timestamp = []
    tot_cases = []

    for el in ids_data:
    	# queries to get timestamp and tot_cases
        s = "select data from regioni where id='" + str(el)+"';"
        timestamp.append(c.execute(s).fetchone())
        s = "select totale_casi from regioni where id='" + str(el)+"';"
        tot_cases.append(c.execute(s).fetchone())

    days = [] #transform timestamps in days
    	
    for el in timestamp:
        days.append(pd.to_datetime(el))
    
    ##settings x axis
    x=md.date2num(days)
    xfmt = md.DateFormatter('%m-%d')
    ax=plt.gca()
    ax.xaxis.set_major_formatter(xfmt)

    plt.title('Data Covid-19',fontsize=8, fontweight='bold')

    ax.set_xlabel('Date')
    ax.set_ylabel('Cases')

    colour = np.random.choice(colours)
    if len(colours) !=1:
    	colours.remove(colour)
    plt.plot(x,tot_cases, colour)
    
    patches.append(mpatches.Patch(color=colour, label=regione))
    i=i+1
    
plt.grid()
plt.legend(handles=patches,loc=2, prop={'size': 6})
plt.savefig("regioni_tot_cases.pdf")
plt.show()

