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
from modelo.TrayectoriaSemantica import TrayectoriasSemantica
from load.Contadores import idUsuario
from SQL import SQLInsert as si
from SQL import SQLSelect as ss
from SQL import SQLUpdate as su
from nominatim import peticion as pet
import numpy as np

start=time()
def cargarDeSQLConceptuales():
    l=ss.cargarTrayectoriasConceptuales()
    print(len(l))
    return l
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
def guardarIdOSM():    
    l=cargarDeSQLConceptuales()
    for i in l:
        l3=list()    
        for j in range(len(i.getGDF())):
            l3.append([j,i.getIdTrayectoria(),pet.getNominatimIdOSM(i.getGDF()["punto"].iloc[j].y,i.getGDF()["punto"].iloc[j].x)])
        su.updateIdOSM(l3)
def probarClasificador(u=1):
    from prediccion import ClasificadorPrediccion as cp
    l=list()
    clasi=cp.ClasificadorPrediccion()
    for i in range(1,2):
        l=probarTrayectoriaSemantica(u=u)
        l4=list()
        ltest=list()
        ltesty=list()
        for i in l:
            l3=list()    
            for j in range(len(i.getDF())):
                idOsm=i.getListOSMId()[j]
                json=pet.getNominatimforId(idOsm)
                if json!=-1:
#                    if json['features'][0]['properties']['type']=='yes':
#                        l3.append(json['features'][0]['properties']['name'])
#                    else:
                    if json['features'][0]['properties']['type']!=l3[-1]:
                        l3.append(json['features'][0]['properties']['type'])
                    
            if len(l3)>2:
                l4.append(l3)
        print(len(l4))
        for i in range(len(l4)-1,-1,-1):
            if i%5==0:
                ltest.append(l4.pop(i))
        clasi.fit(l4)
    for i in ltest:
        ltesty.append(i.pop(-1))

    aciertos=0
    fallos=0
    for j,i in enumerate(ltest):
        pre=clasi.predict(i)
        
        if pre!= None and ltesty[j] in pre:
            aciertos=aciertos+1
        else:
            fallos=fallos+1
    print("Aciertos:",aciertos,"Fallos:",fallos)
    return aciertos,fallos
def probarTrayectoriaSemantica(u=1):
    l=ss.cargarTrayectoriasConceptuales(From="from parado", Where="where  trayectoria.id_usuario="+str(u)+" ")
    ls=list()
    for i in l:
        ls.append(TrayectoriasSemantica(i))
    return ls
from prediccion import Probador as pro
pro.Probador(usuario=153,clasificacion='category')
pro.Probador(usuario=3,clasificacion='category')
pro.Probador(usuario=4,clasificacion='category')
#aciertos=0
#fallos=0
#
#for i in range(0,6):
#    a,f=probarClasificador(u=i)
#    aciertos=aciertos+a
#    fallos=fallos+f
#print("Aciertos:",aciertos,"Fallos:",fallos)
#print("Porcentaje de aciertos:",100/(aciertos+fallos)*aciertos)
#guardarIdOSM()
#cargarDeSQLBrutas()
start=time()-start
print(start)
