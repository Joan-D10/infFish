# -*- coding: utf-8 -*-
"""
N. Ahmad, S. Derrible, T. Eason, and H. Cabezas, 2016, “Using Fisher information to track stability in multivariate systems”,
Royal Society Open Science, 3:160582, DOI: 10.1098/rsos.160582
"""

import csv
import pandas as pd 
import math
import matplotlib.pyplot as plt

def FI(f_name,step,step_1): #se define la función FI, la cual requiere tres variables.
    #f_name=nombre del archivo. step= tamaño de la ventana, step_1= Paso con el que se recorrerá la serie temporal
    
    out=open(f_name+'.csv','r')
    data=csv.reader(out)#abrimos el archivo en modo lectura
    Data=[] #generamos una lista vacía 
        
    for row in data: #para cada lista en el objeto data, la iremos agregando en la lista Data
        Data.append(row)
            
    out.close() #cerramos la base de datos
    
    
    
    
    
    Data_num=[]
    Time=[] #guarda la primera columna como el tiempo
    
    for row in Data: #para cada fila en la lista Data
        Time.append(row[0]) #Se agrega la primera columna de la fila a la lista Time
        temp=[]
        for i in range(1,len(row)):#para cada valor en el rango de 1 al rango de la longitud de la fila
            if row[i]=='':         #si el valor de la posición en esa fila es 0
                temp.append(0)     #se agrega un valor 0 a la lista temp
            else:
                temp.append(float(row[i]))#si no es un valor nulo, entonces se agrega el valor a la lista temp
        Data_num.append(temp)# a la lista Data_num se le agrega la lista temp, que contiene todos los valores menos ls de la
                             #primera columna
        
#    print Time
#    print Data_num
    
    
    out=open('{}_sost.csv'.format(f_name),'r')  #se abre otro archivo con nombre f_name_sost.csv en modo lectura
    #este archivo debe mantener los valores de tolerancia
    data=csv.reader(out) #se genera el objeto en modo lectura
    Data=[]   #volvemos a dejar la lista Data vacía
        
    for row in data: #para cada fila en data
        Data.append(row) #a la lista Data se le agregan esas filas
            
    out.close() #cerramos el archivo
    
    sost=[]     #son los valores de tolerancia
    
    for i in Data[0]:        #para cada elemento en la primer fila
        sost.append(eval(i)) #los valores se convierten en numeros y se agregan a la lista sost
        
#    print sost
    
    FI_final=[]  #
    k_init=[]
    for i in range(0,len(Data_num),step_1): #El código divide los datos en ventanas de tamaño step y las desliza step_1 pasos cada vez. Por cada ventana, se calcula FI.
        
        Data_win=Data_num[i:i+step]   #se guardan los valores de data num que ocupan la posición i a i+step
        win_number=i                  #se crea un win number igual a i
#        if win_number==0:
#            print Data_win , len(Data_win)
       
        if len(Data_win)==step:  #si la longitud de Data win es igual al tamaño de la ventana
            Bin=[]  # Inicializa la matriz de similitud Bin
            for m in range(len( Data_win)): # Itera sobre cada fila de la ventana
                Bin_temp=[]                 # Fila de la matriz Bin
                
                for n in range(len( Data_win)): # Compara con todas las columnas de la ventana
                    if m==n:  
                        Bin_temp.append('I') # Si posicion de columna y fila es la misma, se marca con 'I' (identidad)
                    else:
                        Bin_temp_1=[] # Lista temporal para contar similitudes
                        
                        for k in range(len(Data_win[n])): # Recorre cada variable en la fila
                            if (abs(Data_win[m][k]-Data_win[n][k]))<=sost[k]:
                                Bin_temp_1.append(1) # Si la diferencia es menor que el umbral de tolerancia, se le agrega el valor 1
                            else:
                                Bin_temp_1.append(0)#si no se cumple la condicion, se agrega un 0
                                
                        Bin_temp.append(sum(Bin_temp_1))# a la lista bin temp se le agrega el valor de la suma de bin temp 1
                        
                    
                
                        
                Bin.append(Bin_temp) # y ese valor se agrega a la matriz Bin
                #aclaración: como Bin_temp es una lista, y se van agregando estas listas, el arreglo final es una lista
                #de listas (una matriz)
            
            
#            df=pd.DataFrame(Bin)
#            
#            
#            
#           
#            
#            df.to_csv('bin_{}.csv'.format(i))    
#            
            FI=[]
            for tl in range(1,101):  # Se prueba con diferentes umbrales
                tl1=len(sost)*float(tl)/100 # Umbral basado en el número de variables, tl1 varía desde el 1% hasta el 100% del número total de variables en los datos.
                Bin_1=[]  # Lista de grupos
                Bin_2=[] # Lista de elementos ya agrupados
                
                for j in range(len(Bin)): # Recorremos cada punto de datos

                    if j not in Bin_2: # Si el punto aún no está en un clúster
                        
                        Bin_1_temp=[j] # Creamos un nuevo clúster con el punto actual
                        for i in range(len(Bin[j])): # Creamos un nuevo clúster con el punto actual
                            if Bin[j][i]!='I' and Bin[j][i]>=tl1 and i not in Bin_2:
                                Bin_1_temp.append(i) # Si es similar, lo agregamos al clúster
                                
                        Bin_1.append(Bin_1_temp) # Guardamos el clúster
                        Bin_2.extend(Bin_1_temp) # Marcamos los puntos como agrupados
                    
#                if win_number==0:
#                    print Bin_1 , tl
#Cada clúster se usa para calcular la probabilidad de encontrar un punto en un clúster de cierto tamaño:
                prob=[0] #Se agregan 0 al inicio por condicion de frontera
                for i in Bin_1:
                    prob.append(float(len(i))/len(Bin_2))
                #Ejemplo: Si Bin_1 = [[0, 1, 2], [3, 4]], entonces: El primer clúster tiene 3 elementos de 5 → probabilidad = 3/5 = 0.6
                    
                prob.append(0) #Se agregan 0 al final por condiciones de frontera.
                
               
                prob_q=[]
                for i in prob:
                    prob_q.append(math.sqrt(i)) # Se toma la raíz cuadrada de cada probabilidad
                    
               
                
                FI_temp=0
                for i in range(len(prob_q)-1):
                    FI_temp+=(prob_q[i]-prob_q[i+1])**2 #Diferencias cuadrados en las probabilidades
                FI_temp=4*FI_temp  # Se multiplica por 4 para normalizar  
                
                FI.append(FI_temp) # Se almacena en la lista FI
                
          
            for i in range(len(FI)): #Este bucle recorre todos los valores de la lista FI
                if FI[i]!=8.0: #La condición verifica si el valor de FI[i] no es igual a 8.0.
                    k_init.append(FI.index(FI[i])) #Si se encuentra un valor válido de FI (es decir, distinto de 8.0), el código agrega el índice de ese valor a la lista k_init.
                    #¿Por qué usar FI.index(FI[i])? Esto está buscando el primer índice donde ocurre un valor distinto de 8.0 en la lista FI. Esto se almacena en k_init, que será una lista de los índices en los que la FI cambia de manera significativa.
                    break #Después de agregar el primer índice válido de FI a k_init, el break termina el bucle.
            
                
            FI_final.append(FI)
  
        
    if len(k_init)==0: 
        k_init.append(0)
    for i in range(0,len(FI_final)):
        FI_final[i].append(float(sum(FI_final[i][min(k_init):len(FI_final[i])]))/len(FI_final[i][min(k_init):len(FI_final[i])]))
        FI_final[i].append(Time[(i*step_1+step)-1])
        #Si no se encontró un valor válido en k_init (es decir, si la lista está vacía), se inicializa k_init con el valor 0
        #Para cada sublista en FI_final, se calcula el promedio de FI desde el índice mínimo de k_init hasta el final de la lista, y este promedio se agrega a la sublista.
        #finalmente, se agrega el tiempo correspondiente a esa sublista en FI_final, de manera que cada sublista de FI tiene un valor promedio y su correspondiente valor de tiempo.
        
#    out=open("FI.csv","w")
#    new=csv.writer(out)
#    for i in FI_final:
#        new.writerow(i)
#        
#    out.close()
    
    df_FI=pd.DataFrame(FI_final)
    df_FI.to_csv("FI.csv",index=False,header=False)#este código genera los datos obtenidos en FI en un documento csv.
    
    plt.plot(range(step,len(FI_final)+step),[i[-2] for i in FI_final ],
    'b',label='FI')
    plt.ylim(0,8.5)
    plt.ylabel('Fisher Information')
    plt.xlabel('Time')
    plt.tight_layout()