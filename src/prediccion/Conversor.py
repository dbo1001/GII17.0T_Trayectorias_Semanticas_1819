# -*- coding: utf-8 -*-
"""
Created on Wed May 22 01:40:06 2019

@author: Hector
"""
from modelo import TrayectoriaSemantica 
from nominatim import peticion as pet
import numpy as np
import networkx as nx
class Conversor():
    def __init__(self):
        self.__grap=nx.DiGraph()
        self.__grap.add_nodes_from(['waterway','tourism','telecom','sport','shop','route','railway','public_transport','power','place','office','natural','military','man_made','leisure','landuse','historic','highway','geological','emergency','craft','building','boundary','barrier','amenity','aeroway','aerialway'])
        self.__dict={'waterway':0,'tourism':0,'telecom':0,'sport':0,'shop':0,'route':0,'railway':0,'public_transport':0,'power':0,'place':0,'office':0,'natural':0,'military':0,'man_made':0,'leisure':0,'landuse':0,'historic':0,'highway':0,'geological':0,'emergency':0,'craft':0,'building':0,'boundary':0,'barrier':0,'amenity':0,'aeroway':0,'aerialway':0}
        pass
    def TStoIdOSM(self,lts):
        lista=list()
        for ts in lts:
            if len(ts.getListOSMId())>2:
                lista.append(ts.getListOSMId())
        return lista
    def TCtoTS(self,ltc,tParadas=600):
        lts=list()
        for i in ltc:
            lts.append(TrayectoriaSemantica.TrayectoriasSemantica(i,tParadas=tParadas))
        return lts
    def IdOSMtoMatrizClase(self,lOSM):

        g=self.__grap.copy()
        l=self.combertirACategorias(lOSM)
        contador=0
        for i in l:
            for j in range(len(i)-1):
                try:
                    if g.has_edge(i[j],i[j+1]):  
                        g[i[j]][i[j+1]]['weight'] += 1
                    else:
                        g.add_edge(i[j], i[j+1], weight=1)
                    contador+=1
                except:
                    pass
        r=nx.to_numpy_array(g).flatten()
        if contador!=0:
            return r/contador
        else:
            return r
    def IdOSMtoList(self,lOSM):
        dic=self.__dict.copy()
        l=self.combertirACategorias(lOSM)
        for i in l:
            for j in i:
                dic[j]=dic[j]+1
        return list(dic.values())
    def combertirATipos(self,X):
        '''
        Función que se encarga de convertir las Id de OSM a el tipo que corresponde a esta Id.

        Args:
            X (list(list(int))): Lista con las rutas de Id de OSM que vamos a convertir

        Raises:

        Returns:
            list(list(str)): La lista de ruta ya convertidas en rutas de tipos
        '''
        l=list()
        for i in X:
            l.append(list())
            for j in i:
                json=pet.getNominatimforId(j)
                if json!=-1:
#                    if json['features'][0]['properties']['type']=='yes':
#                        l[len(l)-1].append(json['features'][0]['properties']['name'])
#                    else:
                    l[len(l)-1].append(json['features'][0]['properties']['type'])
        return l
        
    def combertirACategorias(self,X):
        '''
        Función que se encarga de convertir las Id de OSM a la categoría que corresponde a esta Id.

        Args:
            X (list(list(int))): Lista con las rutas de Id de OSM que vamos a convertir

        Raises:

        Returns:
            list(list(str)): La lista de ruta ya convertidas en rutas de categorías
        '''
        l=list()
        for i in X:
            l.append(list())
            for j in i:
                json=pet.getNominatimforId(j)
                if json!=-1:
                    l[len(l)-1].append(json['features'][0]['properties']['category'])
                
        return l
    
       