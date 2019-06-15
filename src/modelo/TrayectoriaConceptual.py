# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 17:31:39 2019

@author: Hector
"""
#import math
from shapely.geometry import  Point
from nominatim import peticion as pet
#from shapely.geometry import LineString
import geopandas as gpd
class TrayectoriaConceptual():
    '''
    Esta clase contiene y crea trayectorias conceptuales. Si recibe una trayectoria norma la convierte en conceptual.
    Si recibe un GeoDataFrame extrae la información para completar los datos de la trayectoria conceptual.

    Args:
        trayectoria (Trayectoria): Es una lista que contiene rutas, estas rutas están formadas por una lista con las Id de OSM de cada punto.
        trayectoria (GeoDataFrame): GeoDataFrame que contiene los datos necesarios para completar la clase TrayectoriaConceptual.
        
    Attributes:
        gdf (GeoDataFrame): Guarda las paradas, tiempos de inicio, tiempos de fin y la id de la trayectoria conceptual.
        __idTrayectoria (int): Id de la trayectoria.
        __idUsuario (int): Id del usuario al que pertenece la trayectoria.
        
    '''
    def __init__(self,trayectoria):
        if isinstance(trayectoria,gpd.GeoDataFrame):
            self.gdf=trayectoria[['punto',"instante_inicio","instante_fin",'id_osm']]
            self.__idTrayectoria=trayectoria.id_trayectoria.iloc[0]
            self.__idUsuario=trayectoria.id_usuario.iloc[0]
        else:
            self.gdf=gpd.GeoDataFrame(columns=['punto','instante_inicio','instante_fin','id_osm'],geometry="punto")
            self.__CombertirAConceptual(trayectoria)
            self.__idTrayectoria=trayectoria.getIdRuta()
            self.__idUsuario=trayectoria.getIdUsuario()
        pass

    def __CombertirAConceptual(self,trayectoria):
        '''
        Función que convierte una trayectoria normal en una trayectoria conceptual

        Args:
            trayectoria (Trayectoria): Objeto de tipo Trayectoria que convertirá en TrayectoriaConceptual

        Raises:

        Returns:
            
        '''
        gdf=trayectoria.GeoDataFrame
        parado=list()
        for i in range(len(gdf)):
            if gdf.estado[i]==1:
                parado.append(i)
            elif len(parado)>0:
                self.__crearParada(parado,gdf)
                parado=list()
        if len(parado)>0:
            self.__crearParada(parado,gdf)
            parado=list()
#        plt=gdf.plot(figsize=(20, 15), color='blue', markersize=5)        
#        plt=self.gdf.plot(figsize=(20, 15),ax=plt, color='red', markersize=50)
        
        pass
    def getIdUsuario(self):
        '''
        Función de tipo GET que retorna la Id del usuario al que pertenece la trayectoria

        Args:
            
        Raises:

        Returns:
            int: Id del Usuario.
            
        '''
        return self.__idUsuario
    def __crearParada(self,lista,gdf):
        '''
        Esta función agrupa las paradas y las añade al GeoDataFrame de la clase dejando como punto de la parada la media de todos los puntos que la forman.

        Args:
            lista (list): Lista con los índices de las paradas que hay que agrupar.
            gdf (GeoDataFrame): GeoDataFrame de la trayectoria que se está tratando de convertir.
            
        Raises:

        Returns:

        '''
        x=0
        y=0
        for i in lista:
           x=x+gdf.punto[i].x
           y=y+gdf.punto[i].y
        p=Point(x/len(lista),y/len(lista))
        self.gdf.loc[len(self.gdf)]=[ p,gdf.instante[lista[0]],gdf.instante[lista[len(lista)-1]],pet.getNominatimIdOSM(y/len(lista),x/len(lista))]
        pass
    def getIdTrayectoria(self):
        '''
        Función de tipo GET que retorna la Id de la trayectoria.

        Args:
            
        Raises:

        Returns:
            int: Id de la trayectoria.
            
        '''
        return self.__idTrayectoria
    def getGDF(self):
        '''
        Función de tipo GET que retorna el GeoDataFrame que contiene las paradas de la trayectoria conceptual.

        Args:
            
        Raises:

        Returns:
            int: GeoDataFrame que contiene las paradas de la trayectoria conceptual.
            
        '''
        return self.gdf
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)