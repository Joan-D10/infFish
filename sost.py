# -*- coding: utf-8 -*-
"""
N. Ahmad, S. Derrible, T. Eason, and H. Cabezas, 2016, “Using Fisher information to track stability in multivariate systems”,
Royal Society Open Science, 3:160582, DOI: 10.1098/rsos.160582
"""
#este código calcula un tamaño de estado característico basado en la desviación estándar de una serie de datos y lo guarda en un archivo CSV
import csv
import pandas as pd
import numpy as np

def SOST(f_name,s_for_sd): # s_for_sd Tamaño de la ventana para calcular la desviación estándar.
    out=open(f_name+'.csv','r')#abre el erchivo en modo lectura
    data=csv.reader(out)#genera un objeto para poder utilizarlo en modo lectura
    Data=[]
        
    for row in data:
        Data.append(row) #cada valor en data se agrega a Data
            
    out.close()#se cierra el documento
    

    Data_num=[]
    
    for row in Data:
        temp=[]
        for i in range(1,len(row)): ## Ignora la primera columna
            if row[i]=='':
                temp.append(0) # Convierte valores vacíos en 0
            else:
                temp.append(float(row[i])) # Convierte los valores en flotantes y los agrega a lista tiempo
        Data_num.append(temp)
        

    df=pd.DataFrame(Data_num) #Esto crea una tabla donde cada columna representa una serie de datos numéricos.
    
    sos=[]
    for j in range(len(df.columns)):# Itera sobre cada columna
        sos_temp=[]
        for i in df.index: # Itera sobre cada fila
            A=list(df[j][i:i+s_for_sd]) # Extrae una ventana de tamaño `s_for_sd`
            A_1=[float(i) for i in A if i!=0 ]  # Elimina ceros
        
            
            if len(A_1)==s_for_sd: # Calcula la desviación estándar con ddof=1
                sos_temp.append(np.std(A_1,ddof=1))
                #Si la ventana tiene suficientes datos (s_for_sd valores), se calcula la desviación estándar (np.std(A_1, ddof=1)).
                
       
        if len(sos_temp)==0:
            sos.append(0)  # Si no hay suficientes datos, se agrega 0 a sos.

        else:
            sos.append(min(sos_temp)*2) # Guarda el mínimo valor de desviación estándar multiplicado por 2
        
    df_sos=pd.DataFrame(sos)
    df_sos=df_sos.transpose()
    df_sos.to_csv('{}_sost.csv'.format(f_name),index=False,header=False)
    #Se convierte sos en un DataFrame y se guarda en un archivo CSV