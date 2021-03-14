# Contenuto
La cartella contiene:
 - degli script awk e bash per ripulire i dati e creare le serie temporali per regione e provincia.
 - uno script python che prende i dati e li mette in una classe implementata come un nested
   dictionary che ne facilita l'accesso e l'utilizzo. Nonchè permette di stampare le serie temporali
   divise per regione.

## parte dati
In questa directory trovate i dati italiani suddivisi in serie-temporali divisi per regione e provincia. 
I dati nella cartella serie_temporali sono aggiornati al 12/03.

Ci sono anche gli script che ho usato (.awk e .sh). 
Per eseguirli è sufficiente rendere tutti i file .sh e .awk eseguibili (tranquilli niente "virus" ;))
 e lanciare il main.
I dati processati sono quelli della cartella [github](https://github.com/pcm-dpc/COVID-19/tree/master/dati-province)).
 
In queste directory ci sono anche 2 file aggiuntivi, 
uno che rappresenta l'ultima aggiunta e uno che contiene tutti i dati assieme, 
questi vanno rimossi prima di eseguire lo script. 
Altrimenti anche il loro contenuto viene processato e i dati in sostanza sono aggiunti 2 volte,
un alternativa, più efficiente, è modificare lo script bash e eseguire gli script awk solo
sul file con tutti i dati assieme.

### Come scaricare dati da github
Uno dei tanti modi puo' essere:
`svn export https://github.com/pcm-dpc/COVID-19/trunk/dati-province`

Che scarica la cartella contenente i dati-provincie nella directory corrente.

## parte python

Lo script python prende i files nella directory serie_temporali e li rende un database.
La struttura dati è conenuta nella classe albero_a2_livelli.py, che implementa
una struttura ad albero utilizzando dictionaries python.

Lo script ha la particolarità di usare pickle per tenere in memoria il database, creando
un file di dump nella stessa cartella e ricaricandolo ogni volta che rieseguo lo script. 
