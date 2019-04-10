# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 18:54:01 2019

@author: Hector
"""

from load.LoadCSV import LoadCSV 
from time import time
from load.CrearTrayectoriaB import CrearTrayectoriaB
from load.ConfiguracionDeLectura import ConfiguracionDeLectura as CDL
from modelo.TrayectoriaConceptual import TrayectoriaConceptual
from load.Contadores import idUsuario
from SQL import SQLInsert as si
from SQL import SQLSelect as ss

start=time()
def cargarDeSQLConceptuales():
    l=ss.cargarTrayectoriasConceptuales()
    print(len(l))
    pass
def cargarDeSQLBrutas():
    l=ss.cargarTrayectoriasBrutas(Where="where public.trayectoria.id_usuario=1")
    print(len(l))
def cargarDatosCSV2SQL():
    contaUsu=idUsuario()
    direccion="E:/TFG/Data"#"E:/TFG/Data GPX"
    exten='.plt'#'.csv'
    x=1 #Longitud
    y=0 #Latitud

    r=list()
    #cdl=CDL(x=3,y=2,t=[1],ts=["%Y-%m-%dT%H:%M:%SZ"],extension=".csv",lineaIni=1)
    cdl=CDL(x=x,y=y,t=[5,6],ts=["%Y-%m-%d","%H:%M:%S"],extension=exten,lineaIni=6)
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
        for j in range(len(r)):
            conceptuales.append(TrayectoriaConceptual(r[j]))
        si.insertUsuarios(usuarios)
        si.insertTrayectoria(r)
        si.insertarTrayectoriaConceptual(conceptuales)
        print(conta)
        r=list()
        conceptuales=list()
        usuarios=list()
        conta+=1
#cargarDeSQLConceptuales()
cargarDeSQLBrutas()
start=time()-start
print(start)
