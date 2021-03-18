
import urllib.request
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import randomcolor
def ModelAndScatterPlot(graphWidth, graphHeight):
    f = plt.figure(figsize=(graphWidth/100.0, graphHeight/100.0), dpi=100)
    axes = f.add_subplot(111)

    # first the raw data as a scatter plot
    axes.plot(xData, yData,  'D')

    # create data for the fitted equation plot
    xModel = np.linspace(min(xData), max(xData))
    yModel = np.polyval(fittedParameters, xModel)

    # now the model as a line plot
    axes.plot(xModel, yModel)

    axes.set_title('numpy polyfit() and polyval() example') # add a title
    axes.set_xlabel('X Data') # X axis data label
    axes.set_ylabel('Y Data') # Y axis data label

    #plt.show()
    #plt.close('all') # clean up after using pyplot


def RegressionErrorPlot(graphWidth, graphHeight):
    f = plt.figure(figsize=(graphWidth/100.0, graphHeight/100.0), dpi=100)
    axes = f.add_subplot(111)

    axes.plot(yData, regressionError, 'D')

    axes.set_title('Regression error') # add a title
    axes.set_xlabel('Y Data') # X axis data label
    axes.set_ylabel('Regression Error') # Y axis data label

    #plt.show()
    #plt.close('all') # clean up after using pyplot




#popolazione regioni
jsonFile = open('path/to/pop.json', 'r') #write your path (pwd)
values_pop = json.load(jsonFile)
df_pop = pd.DataFrame(values_pop)
jsonFile.close()




#vaccini
with urllib.request.urlopen("https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-summary-latest.json") as f:
    values_italia_vax = json.load(f)
    df_vax = pd.DataFrame(values_italia_vax['data'])
    f.close()




regioni1 = df_vax['nome_area'].unique().tolist()
regioni2 = df_regioni['denominazione_regione'].unique().tolist()
regioni3 = df_pop['regione'].unique().tolist()

regioni_out = []
for regione1 in regioni1:
    for regione2 in regioni2:
        if regione1 == regione2:
            regioni_out.append(regione1)
regioni_out = []
regioni_out = regioni_out + regioni3
regioni_out = list(set(regioni_out))

regioni = []
for regione in regioni_out:
    regioni.append(regione)
regioni.remove('')
regioni.sort() 



colors = ["aliceblue","antiquewhite","aqua","aquamarine","azure","beige","bisque","black","blanchedalmond","blue","blueviolet","brown","burlywood","cadetblue","chartreuse","chocolate","coral","cornflowerblue","cornsilk","crimson","cyan","darkblue","darkcyan","darkgoldenrod","darkgray","darkgrey","darkgreen","darkkhaki","darkmagenta","darkolivegreen","darkorange","darkorchid","darkred","darksalmon","darkseagreen","darkslateblue","darkslategray","darkslategrey","darkturquoise","darkviolet","deeppink","deepskyblue","dimgray","dimgrey","dodgerblue","firebrick","floralwhite","forestgreen","fuchsia","gainsboro","ghostwhite","gold","goldenrod","gray","grey","green","greenyellow","honeydew","hotpink","indianred","indigo","ivory","khaki","lavender","lavenderblush","lawngreen","lemonchiffon","lightblue","lightcoral","lightcyan","lightgoldenrodyellow","lightgray","lightgrey","lightgreen","lightpink","lightsalmon","lightseagreen","lightskyblue","lightslategray","lightslategrey","lightsteelblue","lightyellow","lime","limegreen","linen","magenta","maroon","mediumaquamarine","mediumblue","mediumorchid","mediumpurple","mediumseagreen","mediumslateblue","mediumspringgreen","mediumturquoise","mediumvioletred","midnightblue","mintcream","mistyrose","moccasin","navajowhite","navy","oldlace","olive","olivedrab","orange","orangered","orchid","palegoldenrod","palegreen","paleturquoise","palevioletred","papayawhip","peachpuff","peru","pink","plum","powderblue","purple","rebeccapurple","red","rosybrown","royalblue","saddlebrown","salmon","sandybrown","seagreen","seashell","sienna","silver","skyblue","slateblue","slategray","slategrey","snow","springgreen","steelblue","tan","teal","thistle","tomato","turquoise","violet","wheat","white","whitesmoke","yellow","yellowgreen"]
fit_values = []
fig, ax = plt.subplots()
for regione in regioni:

    tot = df_pop[df_pop.regione==regione]['num_residenti'].values
    sum = 0
    y = [] 
   
    for el in df_vax[df_vax.nome_area==regione]['totale'].values:
        sum += el
        y.append(100*sum/tot)
  
    
    import datetime as dt
    from dateutil import parser
    dates = pd.to_datetime(df_vax[df_vax.nome_area==regione]['data_somministrazione']).sort_values()


    idx, val = "indx", "vals"
  
    # initializing empty mesh 
    res = {idx : [], val : []} 
    for id, vl in enumerate(dates): 
        res[idx].append(id) 
        res[val].append(vl) 
   
    x = res['indx']

    X=[]
    Y=[]
    for el in y:
        Y.append(el[0])
    print(Y)
    for el in x:
        X.append(float(el))
    print(X)

    from sklearn.linear_model import LinearRegression
    if len(X)!=0 and len(Y)!=0 and len(X)==len(Y):
        xData = X
        yData = Y
        polynomialOrder = 1 # example linear equation
        # curve fit the test data
        fittedParameters = np.polyfit(xData, yData, polynomialOrder)
        print('Fitted Parameters:', fittedParameters)
        fit_values.append(fittedParameters[0])
        # predict a single value
        print('Single value prediction:', np.polyval(fittedParameters, 0.175))
        # Use polyval to find model predictions
        modelPredictions = np.polyval(fittedParameters, xData)
        regressionError = modelPredictions - yData

        SE = np.square(regressionError) # squared errors
        MSE = np.mean(SE) # mean squared errors
        RMSE = np.sqrt(MSE) # Root Mean Squared Error, RMSE
        Rsquared = 1.0 - (np.var(regressionError) / np.var(yData))
        print('RMSE:', RMSE)
        print('R-squared:', Rsquared)
        print()
       
        # graphics output section
        graphWidth = 800
        graphHeight = 600
        
        
        plt.plot(xData, yData, linewidth=0.4, color=color,linestyle="--")

        # create data for the fitted equation plot
        xModel = np.linspace(min(xData), max(xData))
        yModel = np.polyval(fittedParameters, xModel)
        # now the model as a line plot
        plt.plot(xModel, yModel, label=regione,linewidth=1.3, color=color )
    
        fig.canvas.draw()
        from datetime import date

        today = date.today()
       
        labels = [item.get_text() for item in ax.get_xticklabels()]
        labels[1] = '27 dec'
        labels[-1] = today.strftime("%d %b")

    
plt.legend(loc=2, prop={'size': 9})
plt.grid(color='grey', linestyle='--', linewidth=0.2)
plt.ylabel(ylabel="Percentuale di popolazione vaccinata %")
plt.xlabel(xlabel="Days")
plt.title('Somministrazione di vaccini per regione')
plt.savefig('regioni_fit.png')
plt.show()
print("% points/days speed:")
print()
import math 

speeds = {}

for regione, speed in zip(regioni,fit_values):
    speeds[regione]=speed
print(speeds)
speeds_sorted = dict(sorted(speeds.items(), key=lambda item: item[1]))
print(speeds_sorted)

print()
print("average speed = ", "%.3f" % np.mean(fit_values), "+-", "%.3f" % (np.std(fit_values)/math.sqrt(len(fit_values))))


