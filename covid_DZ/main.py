import matplotlib.pyplot as plt
#plt.rcParams['axes.facecolor'] = 'black'
from database_albero_2livelli import database_albero_2livelli

import pickle

main_dir ="serie_temporali"

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
# 1) creo database se non l'ho già creato in una run
# precedente.
try:
    # provo a caricare db se esiste
    ds = pickle.load(open("database.pickle", "rb"))
except (OSError, IOError) as e:
    # creo un nuovo database
    ds = database_albero_2livelli()
    ds.popola_struttura(main_dir, campi_regioni, campi_provincie)
    # 1.a) le provincie contengono solo dati cumulativi, aggiungo una colonna
    # con le variazioni giornaliere.
    ds.aggiungi_dati_instantanei(nome_col_cumulata='totale_casi', nome_new_col='casi_giornalieri')
    # 1.b) scrivo nella directory corrente un dump del database
    # in modo da poterlo ricaricare in futuro.
    pickle.dump(ds, open("database.pickle", "wb"))

# INFINE PLOT
# 3) plotto le serie temporali di singole regioni e delle provincie
# che vi appartengono.

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(1, 1, 1)

#ds.stampa_province(ax, 'Puglia', prov_field='casi_giornalieri')
ds.stampa_regioni(ax, "deceduti",["Sardegna","Lombardia", "Lazio", "Veneto", "Puglia"])

# styling grafico
f_size=15
ax.tick_params(which='major', width=1.0, labelsize=f_size)
ax.tick_params(which='major', length=10, labelsize=f_size)

plt.show()
