# Contenuto
In questa directory trovate i file suddivisi in serie-temporali suddivisi per regione e provincia(Italia). I dati nella cartella serie_temporali sono aggiornati al 12/03.

Ci sono anche gli script che ho usato (.awk e .sh). Per eseguirli è sufficiente rendere tutti i file .sh e .awk eseguibili (tranquilli niente "virus" ;)) e lanciare il main.
I dati processati sono quelli ufficiali, (nella cartella [github](https://github.com/pcm-dpc/COVID-19/tree/master/dati-province)), dentro però ci sono anche 2 file aggiuntivi, uno che rappresenta l'ultima aggiunta e uno che contiene tutti i dati assieme, questi vanno rimossi prima di eseguire lo script. (altrimenti anche il loro contenuto viene processato e i dati in sostanza sono aggiunti 2 volte).

## Come scaricare dati da github
Uno dei tanti modi puo' essere:
`svn export https://github.com/pcm-dpc/COVID-19/trunk/dati-province`

Che scarica la cartella contenente i dati-provincie nella directory corrente.
