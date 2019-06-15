# -*- coding: utf-8 -*-
"""
Created on Wed May 22 01:56:32 2019

@author: Hector
"""

from prediccion import ClasificadorPrediccion as cp
import pandas as pd
import numpy as np
from prediccion import Conversor as con

class Probador():
    
    '''
    La clase probador nos sirve para probar distintas configuraciones para utilizar el clasificador de predicción.

    Args:
        X (list(list(int))): Es una lista que contiene rutas, estas rutas están formadas por una lista con las Id de OSM de cada punto.
        
    Attributes:
        __X (list(list(int))): Guarda el argumento X
        __tam (int): Almacena el número de trayectorias
        __estadisticos (DataFrame): Almacena los resultados de cada validación cruzada junto a los parámetros de la validación
        
    '''
    def __init__(self,X):
        self.__X=X
        self.__tam=len(self.__X)
        self.__estadisticos=pd.DataFrame(columns=["Tipo","MinSupport","Division","FMeasure","Precision","Recall","Aciertos","Fallos"])
        self.__conversor=con.Conversor()
        pass
    
    def validacionCruzada(self,tipo,division=5,minSupport=0.05):
        '''
        Esta función realiza la validación cruzada sobre los datos de la clase (__X) y almacena los resultados en __estadisticos

        Args:
            tipo (str): La característica de los puntos que se quiere predecir
            division (int): El numero de divisiones que utilizaremos en la validación cruzada
            minSupport (float): El soporte mínimo que vamos a utilizar en el clasificador durante esta validación

        Raises:

        Returns:
            bool: True Si finaliza correctamente
        '''
        gruposX=list()
        resulY=list()
        clasificadores=list()
        aciertos=0
        fallos=0
        X=self.__X.copy()
        fTipo={"type":self.__conversor.combertirATipos,"category":self.__conversor.combertirACategorias}
        X=fTipo[tipo](X)
        for i in range(division):
            gruposX.append(list())
            resulY.append(list())
            clasificadores.append(cp.ClasificadorPrediccion(minSupport=minSupport))
        while len(X)>0:
            for i in range(len(gruposX)):
                if len(X)>0:
                    gruposX[i].append(X.pop(np.random.randint(len(X))))
        rutaY=gruposX.copy()
        for c,i in enumerate(rutaY):
            for j in i:
                resulY[c].append(j.pop(-1))
        for i in range(division):
            for j in range(division):
                if i!=j:
                    clasificadores[i].fit(gruposX[j])
            a,f=self.__resultados(clasificadores[i],rutaY[i],resulY[i])
            aciertos=aciertos+a
            fallos=fallos+f
        precision=aciertos/(aciertos+fallos)
        recall=(aciertos+fallos)/(self.__tam)
        fmeasure=(2*precision*recall)/(precision+recall)
        self.__estadisticos.loc[len(self.__estadisticos)]=[tipo,minSupport,division,fmeasure,precision,recall,aciertos,fallos]

    def __resultados(self,clasi,ruta,resul):
        '''
        Esta función sirve para contar el numero de aciertos y de fallos que se comenten al intentar predecir una lista de rutas.

        Args:
            clasi (ClasificadorPrediccion): Clasificador entrenado que utilizaremos para hacer las predicciones
            ruta (list(list(str))): Lista con rutas para probar el clasificador
            resul (list(str)): Lista de resultados que tenemos que obtener de las rutas

        Raises:

        Returns:
            int: Número de aciertos
            int: Número de fallos
        '''
        aciertos=0
        fallos=0
        for j,i in enumerate(ruta):
            pre=clasi.predict(i)
            if pre!= None and resul[j] in pre:
                aciertos=aciertos+1
            else:
                fallos=fallos+1

        return aciertos,fallos


    def getEstadisticos(self):
        '''
        Función get que devuelve el DataFrame con los resultados de las validaciones cruzadas.

        Args:

        Raises:

        Returns:
            DataDrame: Contiene los resultados de las validaciones cruzadas
        '''
        return self.__estadisticos
    def graficos(self):
        
        
        self.__estadisticos[["MinSupport","FMeasure"]].plot()
        pass