# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 18:54:01 2019

@author: Hector
"""

from load.LoadCSV import LoadCSV 
from time import time





from load.CrearTrayectoria import CrearTrayectoria
start=time()
direccion="E:/TFG/Data Reducido"
exten='.plt'
x=1 #Longitud
y=0 #Latitud

r=list()


conta=0

lectorCSV=LoadCSV(x,y,[(5,"%Y-%m-%d"),(6,"%H:%M:%S")],exten,'epsg:4326')
for i in lectorCSV.rutasPorUsuario(direccion):
    
    procesar=CrearTrayectoria(args=[i,0,0,1,2,3])
    r.extend(procesar.run())

    conta+=1
    #break

start=time()-start
print(start)