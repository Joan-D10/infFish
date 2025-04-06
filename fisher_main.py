# -*- coding: utf-8 -*-
"""
N. Ahmad, S. Derrible, T. Eason, and H. Cabezas, 2016, “Using Fisher information to track stability in multivariate systems”,
Royal Society Open Science, 3:160582, DOI: 10.1098/rsos.160582
"""
import datetime
import os

Time=datetime.datetime.now() #guarda el tiempo actual en que se ejecuta 

f_name=input('enter file name-') #ingresas el nombre del archivo
w_size=int(input('enter window size-'))#ingresas el tamaño de la ventana
w_incre=int(input('enter window increment-'))#se ingrea el incremento de la ventana (cómo se irá desplazando)
sm_step=int(input('enter step for block average for smoothing of the FI-')) #Parámetro para suavizar la Información de Fisher.
# Si sm_step es muy pequeño, el suavizado será casi imperceptible, y si es demasiado grande, se puede perder información relevante
#pequeño (ej. 3-5). más grande (ej. 10-20)
#Regla empírica: comienza con sm_step ≈ w_size / 10
X_tick=input('Provide step for xticks(Y)-') #Determina si se especificará un paso personalizado para los ejes X.
if X_tick.upper()=='Y':
    xtick_step=int(input('enter step for xticks-'))
else:
    xtick_step='def'
def main(f_name,w_size,w_incre,xtick_step):#definimos funcion
    #Se pregunta al usuario si desea usar un tamaño de estado predeterminado (Y) o cargar un archivo con estados (file_name_sost.csv).
    
    if input('''Want to use default size of state? enter Y  
    otherwise enter N and provide a .csv file named 'file name'_sost.csv-''')=='Y':
        from sost import SOST #del código sost, importa SOST
        SOST(f_name,w_size) #y le pasa el nombre del archivo con su tamaño
    from fisher import FI 
    FI(f_name,w_size,w_incre) #del código fisher, importa FI y le pasa el nombre, el tamaño de ventana y el incremento
    
    from smooth import FI_smooth #del código smooth importa FI_smooth
    FI_smooth(f_name,sm_step,w_size,xtick_step) #y mete el nombre, los pasos, el tamaño de ventana, y  ¿xtick?
    
    

main(f_name,w_size,w_incre,xtick_step)#se usa la función
os.remove('FI.csv') #Se elimina el archivo FI.csv, que probablemente sea un archivo temporal.
print ('Total time taken-',datetime.datetime.now()-Time) #Se muestra el tiempo total de ejecución.