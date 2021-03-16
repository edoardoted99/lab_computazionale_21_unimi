import os
import pandas as pd

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
class database_albero_2livelli:
    """
    Questa classe gestisce la struttura dati, organizza i dati come nested
    dictionary. I dataframe si trovano solo al secondo livello.
    In particolare al primo livello seleziono la regione e al secondo
    le provincie o dati relativi all'intera regione.
    """
    """
    esempio, caso 2 regioni, 2 provincie.
      |
     / \
    /   \        
   /\   /\      Livello 1
  /  \ /  \
  A  B C  D     Livello 2
    """
    def __init__(self):
        self.d={} # creo il dictionary
        # queste stringhe inutilmente complicate sono solo per
        # rendere più agevole riciclare la calsse in futuro
        self.reg_string="regione"
        self.extension=".csv"
        self.reg_file=self.reg_string+self.extension
        # ho integrato parte dello styling nella classe.
        self.font_size=15

    def popola_struttura(self, in_dir, campi_regione, campi_provincie):
        """
        Questa funzione prende in ingresso una directory strutturata in
        albero a 2 livelli e pone il contenuto in un nested dictionary: self.d.
        :param in_dir:  string
            percorso alla directory con i dati
        :param campi_regione:
            campi nei file regione che vogliamo importare
        :param campi_provincie:
            campi nei file provincie che vogliamo importare
        :return: none
        """
        # leggo i nomi delle directory del primo livello
        regioni = next(os.walk(in_dir))[1]
        # per ogni directory costruisco il secondo livello
        for reg in regioni:
        # creo una lista con il nome delle provincie
            provincie = next(os.walk(in_dir+"/"+reg))[2]
        # creo il secondo livello per il branch corrente
            self.d[reg]={}
            for prov in provincie:
            # gestisco il caso perticolare per distinguere
            # dati circa l'intera regione o di una specifica
            # provincia.
                if prov==self.reg_file:
                    campi=campi_regione
                else:
                    campi=campi_provincie
            # leggo i files dalla cartella serie temporali.
            # assumo che l'estensione del file sia di 3 caratteri eg.
            # .txt, .dat, .csv
            # TODO: get_df assume il separatore sia la virgola, modificare in futuro.
                self.d[reg][prov[:-4]] = get_df(in_dir+"/"+reg+"/"+prov,
                                   campi)
    def aggiungi_dati_instantanei(self,nome_col_cumulata, nome_new_col="", regione=False):
        """
        Siccome in alcuni casi nei files letti compaiono solo dati cumulativi
        con questa funzione aggiungo una colonna al dataframes contenente
        i dati instantanei(i.e. variazioe giornaliera dati cumulativi).
        :param nome_col_cumulata: STRING
        Colonna che contiene i dati cumulativi
        :param nome_new_col: STRING
        Nome della nuova colonna che vogliamo creare
        :param regione: BOOL
        True se vogliamo che l'operazione sia eseguita anche sui file
        relativi all'intera regione.
        :return:
        """
        for reg in self.d.keys():
            for key, df in self.d[reg].items():
                if key == self.reg_string:
                # se il database corrente è quello della regione
                # aggiungo la colonna solo se l'opzione regione è on.
                    if regione:
                        inst_data(df, nome_col_cumulata, nome_new_col)
                else:
                # se il database corrente è quello di una provincia
                # aggiungo la colonna solo se l'opzione regione è off.
                    if not regione:
                        inst_data(df, nome_col_cumulata, nome_new_col)

    def stampa_province(self, ax, nome_regione, campo="casi_giornalieri"):
        """
        La funzione plotta sull'asse ax il campo prov_field per le
        provincie e re_field per le regioni.
        :param ax:
        asse su cui plottare i dati.
        :param nome_regione:
        nome regione che vogliamo plottare
        :param prov_field:
        :param re_field:
        :param stampa_cumulativo:
        :return: none
        """
        for key, df in self.d[nome_regione].items():
            self.make_printable(df)
            if key != self.reg_string:
                ax = df[campo].plot(label=key)
        ax.legend(fontsize=self.font_size, title="Provincie", title_fontsize=self.font_size)
        ax.set_xlabel("data", fontsize=self.font_size)
        ax.set_ylabel(campo, fontsize=self.font_size)
    def stampa_regioni(self, ax, campo, regioni=[]):
        """
        Stampa sull'asse le serie temporali del campo scelto, per
        le regioni selezionate, o tutte (default)
        :param ax:
        asse su cui stampare
        :param ax:
        campo delle regioni che vogliamo stampare
        :param regioni: lista di stringhe (opzionale)
        permette di stampare solo un numero limitato di regioni
        :return:
        """
        # se non è specificata una regione le stampo tutte
        if not regioni:
            regioni= self.d.keys()

        for reg in regioni:
            ax = self.d[reg][self.reg_string][campo].plot(label=reg)
        ax.legend(fontsize=self.font_size, title="Regioni", title_fontsize=self.font_size)
        ax.set_xlabel("data", fontsize=self.font_size)
        ax.set_ylabel(campo, fontsize=self.font_size)


    def make_printable(self, df):
        # per fare un plot con date sull'asse da stack
        # overflow consigliano questo trick.
        # dove 'data' è il nome della colonna su cui ho la data.
        df['data'] = pd.to_datetime(df['data'],
                                    format="%d.%m.%Y %H:%M:%S.%f")
        df.set_index('data', inplace=True)
