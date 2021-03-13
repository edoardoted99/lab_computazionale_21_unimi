import pandas as pd
import matplotlib.pyplot as plt
#plt.rcParams['axes.facecolor'] = 'black'
import os

# some functions used in the script
def get_df(path ,campi):
    return pd.read_csv(
        path,
        sep=',',
        usecols=campi,  # Only load
        parse_dates=['data']  # Intepret the birth_dat
        # skiprows =10 ,
        # Skip the first 10 rows of
    )
def inst_data(df, col_cumulativa, new_col=""):
    # if no column name is given take the current one and add a
    # delta
    if new_col == "":
        new_col = "delta_" + col_cumulativa
    temp = [
        df[col_cumulativa][i]-df[col_cumulativa][i-1]
        for i in range(1,len(df.index))
    ]
    temp.insert(0, 0)
    # il loop lascia fuori il primo elemento
    df[new_col]=temp
def stampa_regione(ax, dict, prov_field="casi_giornalieri",
                   re_field="nuovi_positivi", stampa_cumulativo=False):
    """
    La funzione plotta sull'asse ax il campo casi giornalieri
    per le provincie e re_field per le regioni.
    :param ax:
    asse su cui plottare i dati.
    :param dict:
    il parametro di intgresso dovrebbe essere un dizionario
    contenente i dataframe di una certa regione.
    :return: nothing
    """
    for df in dict.values():
        df['data'] = pd.to_datetime(df['data'],
                                      format="%d.%m.%Y %H:%M:%S.%f")
        df.set_index('data', inplace=True)
        if df.name != 'regione':
            ax = df[prov_field].plot(label=df.name)
        else:
            if stampa_cumulativo:
                ax=df[re_field].plot(label=df.name)

main_dir ="serie_temporali/"

# seleziono i campi csv desiderati:
campi_provincie = [ 'data', 'totale_casi' ]
campi_regioni = ["data","ricoverati_con_sintomi", "terapia_intensiva",
                 "totale_ospedalizzati","isolamento_domiciliare",
                 "totale_positivi","variazione_totale_positivi",
                 "nuovi_positivi","dimessi_guariti","deceduti",
                 "casi_da_sospetto_diagnostico","casi_da_screening",
                 "totale_casi","tamponi","casi_testati","note",
                 "ingressi_terapia_intensiva"]


# INIZIO PROGRAMMA:
# 1) creo database
# get a list of regioni
regioni= next(os.walk(main_dir))[1]
# è tipo ls -d, però restituise una lista python

# struttura dati: nested dictionary
# d è un dictionary, ha come voci il nome delle provincie italiane
# a ogni voce corrisponde un altro dizionario che contiene come valori
# i dataframe associati a quella regione.
"""
ad esempio:
d
|_Lombardia
|           |_Sondrio
|           |_Bergamo 
|           |_Brescia
|           |_Milano
|           .
.           .
.
"""

d = {}

for reg in regioni:
    # creo una lista con il nome delle provincie
    provincie = next(os.walk(main_dir+"/"+reg))[2]
    d[reg]={}
    for prov in provincie:
        if prov=="regione.csv":
            campi=campi_regioni
        else:
            campi=campi_provincie
        # leggo i files dalla cartella serie temporali.
        d[reg][prov[:-4]] = get_df(main_dir+"/"+reg+"/"+prov,
                                   campi)
        # make the dataframe has the same name as the key in the
        # dictionary.
        d[reg][prov[:-4]].name = prov[:-4]



# 2) le provincie contengono solo dati cumulativi, aggiungo una colonna
# con le variazioni giornaliere.

for reg in regioni:
    for df in d["Lombardia"].values():
        if df.name != 'regione':
            inst_data(df, 'totale_casi', new_col="casi_giornalieri")

# INFINE PLOT
# 3) plotto le serie temporali di singole regioni e delle provincie
# che vi appartengono.

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(1, 1, 1)

# Stampo sullo stesso grafo il numero di casi giornalieri per provincia
# in questo caso della lombardia.
stampa_regione(ax, d["Lombardia"], prov_field='casi_giornalieri')

f_size=15
ax.tick_params(which='major', width=1.0, labelsize=f_size)
ax.tick_params(which='major', length=10, labelsize=f_size)

ax.legend(fontsize=10, title='Provincie Lom',title_fontsize=15)
ax.set_xlabel("data", fontsize=f_size)
ax.set_ylabel("tamponi positivi giornalieri", fontsize=f_size)

plt.show()


