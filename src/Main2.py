# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 18:54:01 2019

@author: Hector
"""

from load.LoadCSV import LoadCSV 
from time import time
from load.CrearTrayectoriaB import CrearTrayectoriaB
from modelo.Estadisticas import Estadisticas
from load.ConfiguracionDeLectura import ConfiguracionDeLectura as CDL
from modelo.TrayectoriaConceptual import TrayectoriaConceptual
from load.Contadores import idUsuario
from SQL import SQLInsert as si
contaUsu=idUsuario()
start=time()
direccion="E:/TFG/Data GPX"#"E:/TFG/Data Reducido"
exten='.csv'#'.plt'
x=1 #Longitud
y=0 #Latitud
estadisticas=Estadisticas()
r=list()
cdl=CDL(x=3,y=2,t=[1],ts=["%Y-%m-%dT%H:%M:%SZ"],extension=".csv",lineaIni=1)
usuarios=list()
conceptuales=list()
conta=0

#lectorCSV=LoadCSV(x,y,[(5,"%Y-%m-%d"),(6,"%H:%M:%S")],exten,'epsg:4326',6)
lectorCSV=LoadCSV(cdl)
for i in lectorCSV.rutasPorUsuario(direccion):
    usuario=contaUsu.cId()
    usuarios.append(usuario)
    procesar=CrearTrayectoriaB(args=[i,usuario,0,1,2,3])
    r.extend(procesar.run())

    conta+=1
    if conta==1:
        break
print('Porcentajede paradas: '+str(estadisticas.porcentajeDeParadas(r))+'%')

for i in range(len(r)):
    print('=============================================================================')
    print('Rura:',r[i].getIdRuta(),"Usuario:",r[i].getIdUsuario())
#    r[i].plotTrayectoria()
    conceptuales.append(TrayectoriaConceptual(r[i]))
    print('Velocidad media parado:',r[i].velocidadMediaParado(),'m/s')
    print('Velocidad media en movimiento:',r[i].velocidadMediaMovimiento(),'m/s')
    print('Velocidad media puntos sin definir:',r[i].velocidadMediaSinDefinir(),'m/s')
    print('=============================================================================')
print(len(r))
start=time()-start
print(start)
print(si.insertUsuarios(usuarios))
print(si.insertTrayectoria(r))
print(si.insertarTrayectoriaConceptual(conceptuales))