# -*- coding: utf-8 -*-
"""
Created on Mon May 20 17:13:07 2019

@author: Hector
"""
from prediccion import ClasificadorPrediccion as cp
from SQL import SQLSelect as ss
from modelo.TrayectoriaSemantica import TrayectoriasSemantica
import numpy as np
from nominatim import peticion as pet
class Probador():
    def __init__(self,usuario=35,clasificacion='type'):
        self.__usuario=usuario
        self.__X=self.__cargarUsuario()
        if clasificacion=='type':
            self.__combertirATipos()
        self.estadoDeDatos()
        self.validacionCruzada()
        pass
    def validacionCruzada(self,division=5):
        gruposX=list()
        resulY=list()
        clasificadores=list()
        for i in range(division):
            gruposX.append(list())
            resulY.append(list())
            clasificadores.append(cp.ClasificadorPrediccion())
        while len(self.__X)>0:
            for i in range(len(gruposX)):
                if len(self.__X)>0:
                    gruposX[i].append(self.__X.pop(np.random.randint(len(self.__X))))
        rutaY=gruposX.copy()
        for c,i in enumerate(rutaY):
            for j in i:
                print(j)
                resulY[c].append(j.pop(-1))
        for i in range(division):
            for j in range(division):
                if i!=j:
                    clasificadores[i].fit(gruposX[j])
            self.resultadosTop3(clasificadores[i],rutaY[i],resulY[i])
        pass
    def resultadosTop3(self,clasi,ruta,resul):
        aciertos=0
        fallos=0
        for j,i in enumerate(ruta):
            pre=clasi.predict(i)
            if pre!= None and resul[j] in pre:
                aciertos=aciertos+1
            else:
                fallos=fallos+1
        print("Aciertos:",aciertos,"Fallos:",fallos)
        pass
    def resutadoUnico():
        pass
    def estadisticas():
        pass
    def __cargarUsuario(self):
        #for d in range (1,8):
        l=ss.cargarTrayectoriasConceptuales(From="from parado", Where="where  trayectoria.id_usuario="+str(self.__usuario)+" ")
        #and EXTRACT(ISODOW FROM parado.instante_inicio) IN ("+str(d)+")
        ls=list()
        for i in l:
            if len(TrayectoriasSemantica(i).getListOSMId())>2:
                ls.append(TrayectoriasSemantica(i).getListOSMId())
        return ls
    def __combertirATipos(self):
        l=list()
        for i in self.__X:
            l.append(list())
            for j in i:
                json=pet.getNominatimforId(j)
                if json!=-1:
#                    if json['features'][0]['properties']['type']=='yes':
#                        l[len(l)-1].append(json['features'][0]['properties']['name'])
#                    else:
                    l[len(l)-1].append(json['features'][0]['properties']['type'])
                
        self.__X=l
    
    def estadoDeDatos(self):
        variabilidad=dict()
        contaPuntos=0
        for i in self.__X:
            for j in i:
                contaPuntos=contaPuntos+1
                if j in variabilidad:
                    variabilidad[j]=variabilidad[j]+1
                else:
                    variabilidad[j]=1
        print("---------------------------------")
        l=list(variabilidad.values())
        media=np.mean(l)
        desviacion=0
        for i in l:
            desviacion=desviacion+(i-media)**2
        desviacion=desviacion/(len(l)-1)
        varianza=desviacion**2
        print("Clases: ",len(variabilidad),"Elementos: ",contaPuntos,'Desviacion: ',desviacion,'Varianza: ',varianza)