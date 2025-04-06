# -*- coding: utf-8 -*-
"""
N. Ahmad, S. Derrible, T. Eason, and H. Cabezas, 2016, “Using Fisher information to track stability in multivariate systems”,
Royal Society Open Science, 3:160582, DOI: 10.1098/rsos.160582
"""

import csv
import matplotlib.pyplot as plt
import pandas as pd
#este código suaviza la información de fisher
def FI_smooth(f_name,step,step_win,xtick_step):
    out=open('FI.csv','r')#abre un archivo FI.csv
    data=csv.reader(out) #y crea un cursor en modo abrir
    Data=[]
        
    for row in data: #para cada dato en el documento
        Data.append(row) #se agrega a la lista Data
            
    out.close()#cerramos el documento
    
    FI=[]
    time=[]
    
    for row in Data:
        FI.append(eval(row[-2])) #Se extraen las dos últimas columnas de cada row
        time.append(row[-1]) # Tiempos correspondientes a cada valor de FI.
        
    FI_smth=[]
    
   
    for i in range(step,len(FI)+step,step): #Se calcula un promedio móvil de los valores de FI en bloques de tamaño step
        for j in range(i-step,i):
            FI_smth.append(float(sum(FI[i-step:i]))/len(FI[i-step:i]))
            
    FI_smth=FI_smth[0:len(FI)] #Se asegura que la lista FI_smth tenga la misma longitud que FI.
            
 
    plt.plot(range(step_win,len(FI_smth)+step_win),FI_smth,'r',label='Smoothed') #Dibuja la curva de FI_smth en color rojo ('r').
    plt.xlabel('Time Step')
    plt.ylabel('Fisher Information')
    
    if xtick_step!='def': #Si el usuario proporciona xtick_step, usa ese valor para espaciar las marcas en el eje X.
        plt.xticks(range(step_win,len(FI_smth)+step_win,xtick_step),
                [time[i] for i in range(0,len(FI_smth),xtick_step)],rotation=75)
                
    else: #Si no, usa un valor predeterminado de 3.
        plt.xticks(range(step_win,len(FI_smth)+step_win,3),
                [time[i] for i in range(0,len(FI_smth),3)],rotation=75)
        
    plt.legend()
    plt.tight_layout()
    plt.savefig(f_name+'_FI'+'.pdf') #Guarda la gráfica en PDF y PNG con nombre basado en f_name
    plt.savefig(f_name+'_FI'+'.png',dpi=1000) #dpi=1000 asegura alta resolución para la imagen.
    plt.close('all') #plt.close('all') cierra todas las figuras para liberar memoria.
    
    
    out=open('FI.csv','r') #Se vuelve a leer el archivo FI.csv para añadir la columna suavizada
    data=csv.reader(out)
    Data=[]
        
    for row in data:
        Data.append(row)
            
    out.close()
    
    for i in range(len(Data)):
        Data[i].append(FI_smth[i])
    
#    out=open("%s_FI.csv"%(f_name),"w")
#    new=csv.writer(out)
#    
#
#    new.writerow(['Time_Step','FI','Smooth_FI'])
    data_final=[] #data_final almacena solo las columnas necesarias (Time_Step, FI, Smooth_FI).
    for i in Data:
        data_temp=[i[-2],i[-3],i[-1]]
        data_final.append(data_temp)
    
    df_final=pd.DataFrame(data_final) #Se usa pandas.DataFrame para estructurar los datos.
    df_final.columns=['Time_Step','FI','Smooth_FI']
    df_final.to_csv("%s_FI.csv"%(f_name)) #Se guarda en un nuevo archivo f_name_FI.csv.
      #El método .to_csv(...) de pandas exporta el contenido del DataFrame a un archivo CSV.  
    #out.close()