# Contenuto
La cartella contiene:
 - degli script awk e bash per ripulire i dati e creare le serie temporali per regione e provincia.
 - uno script python che prende i dati e li mette in una classe implementata come un nested
   dictionary che ne facilita l'accesso e l'utilizzo. Nonchè permette di stampare le serie temporali
   divise per regione.

## parte dati
In questa directory trovate i dati italiani 
suddivisi in serie-temporali divisi per regione e 
provincia. 
I dati nella cartella serie_temporali sono aggiornati
 al 16/03.

Ci sono anche gli script che ho usato (.awk e .sh). 
Per eseguirli è sufficiente rendere main.sh 
e i due script.awk eseguibili (tranquilli niente 
"virus" ;)) e lanciare il main.
I file processati sono quelli aggregati, uno per 
regione e uno per la provincia, tipo
[questo]("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv")


## parte python

Lo script python prende i files nella directory 
serie_temporali e li rende un database.
La struttura dati è conenuta nella classe 
database_albero_a2_livelli.py, che implementa
una struttura ad albero utilizzando dictionaries 
python.

Lo script ha la particolarità di usare pickle per 
tenere in memoria il database, creando un file di 
dump nella stessa cartella e ricaricandolo ogni 
volta che rieseguo lo script. 

Per il momento le funzionalità sono plottare uno 
specifico campo per un insieme arbitrario di regioni.
E plottare i casi giornalieri per tutte le provincie
 in una data regione.

### funzionalità Pycharm
Se si usa in IDE, tipo pycharm (che consiglio), 
quando si fa un plot è sempre possibile fare zoom 
arbitrari sui dati, rendendo in prima battuata non 
necessario implementare un metodo per selezionare 
sequenze temporali.

Altre funzionalità utili di Pycharm sono:
 - autocompletion, dei metodi delle funzioni e 
  nome delle variabili
 - quando si chiama una funzione suggerisce il nome e 
  posizione dei vari argomenti.
 - permette di compattare il codice di funzioni e classi
  il che rende navigare tra il codice in modo molto
  più rapido e semplice.

Rispetto a jupyter ha lo svantaggio di non tenere in
memoria i dati del precedente run, ma a ciò si può
ovviare con [pickle](https://www.thoughtco.com/using-pickle-to-save-objects-2813661)
, se necessario. Inoltre i pacchetti vanno aggiunti 
a mano quando servono, e configurare l'interprete 
può non essere immediato.
