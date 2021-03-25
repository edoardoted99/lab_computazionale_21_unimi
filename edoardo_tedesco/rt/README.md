Questo è lo script per scaricare i dati dei report settimanali relativi al tasso Rt


```console
pip3 install -r requirements.txt
python3 scrape_rt.py
```
I file vengono scaricati dal seguente archivio:

http://www.salute.gov.it/portale/nuovocoronavirus/archivioNotizieNuovoCoronavirus.jsp?lingua=italiano&tipo=Report+settimanale+Covid-19&btnCerca=cerca


Example output:

|nome_regione  |Rt  |data      |
|--------------|----|----------|
|Abruzzo       |1.05|2021-01-17|
|Abruzzo       |1.12|2021-01-10|
|Basilicata    |1.22|2021-01-10|
|Basilicata    |0.9 |2021-01-02|


&nbsp;

Example pdf to scrape:

http://www.salute.gov.it/imgs/C_17_monitoraggi_49_0_fileRegionale.pdf

http://www.salute.gov.it/portale/news/documenti/Epi_aggiornamenti/Emilia-Romagna_20200804.pdf



