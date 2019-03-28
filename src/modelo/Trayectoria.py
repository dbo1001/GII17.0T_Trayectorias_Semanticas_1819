# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 18:45:50 2019

@author: Hector
"""
import numpy as np
import geopandas as gpd

class Trayectoria():
    def __init__(self,idr,idu,gdf: gpd.GeoDataFrame):
        self.idRuta=idr
        self.idUsuario=idu
        gdf=gdf.reset_index(drop=True)
        self.T0=60
        self.D0=40
        self.D1=45
        self.crs=gdf.punto.crs
        #Cargar de una base de datos
        if len(list(gdf.columns))==3:
            gdf=CrearTrayectoriaB().CalcularDatos( gdf,self.crs)
        else:
            #Cargar de cero
            self.GeoDataFrame=self.__ObtenerParadas(gdf)
        pass
    def __str__(self):
        return(str(self.GeoDataFrame['estado']))
    def getNumElementos(self):
        """
        >>> from shapely.geometry import Point
        >>> d = {'instante': [1, 2,4],'punto':[Point(1,5),Point(3,3),Point(2,1)],'metros':[30,65,76],'velocidad':[1.3,2.0,7.4], 'estado': [True, True, False]}
        >>> df = gpd.GeoDataFrame(data=d)        
        >>> t=Trayectoria(1,1,df)        
        >>> t.getNumElementos()
        3
        """
        return self.GeoDataFrame.shape[0]
    
    def getIdUsuario(self):
        """
        >>> from shapely.geometry import Point
        >>> d = {'instante': [1, 2,4],'punto':[Point(1,5),Point(3,3),Point(2,1)],'metros':[30,65,76],'velocidad':[1.3,2.0,7.4], 'estado': [True, True, False]}
        >>> df = gpd.GeoDataFrame(data=d)        
        >>> t=Trayectoria(1,1,df) 
        >>> t.getIdUsuario()
        1
        """
        return self.idUsuario
    
    def getIdRuta(self):
        """
        >>> from shapely.geometry import Point
        >>> d = {'instante': [1, 2,4],'punto':[Point(1,5),Point(3,3),Point(2,1)],'metros':[30,65,76],'velocidad':[1.3,2.0,7.4], 'estado': [True, True, False]}
        >>> df = gpd.GeoDataFrame(data=d)        
        >>> t=Trayectoria(1,1,df) 
        >>> t.getIdRuta()
        1
        """
        return self.idRuta
    
    def numParados(self):
        """
        >>> from shapely.geometry import Point
        >>> d = {'instante': [1, 2,4],'punto':[Point(1,5),Point(3,3),Point(2,1)],'metros':[30,65,76],'velocidad':[1.3,2.0,7.4], 'estado': [True, True, False]}
        >>> df = gpd.GeoDataFrame(data=d)        
        >>> t=Trayectoria(1,1,df) 
        >>> t.numestados()
        2
        """
        try:
            r=self.GeoDataFrame['estado'].value_counts()[1]
        except:
            r=0
        return r
    
    def getExtremos(self):
        """
        
        """
        self.GeoDataFrame.apply()
        pass 
    
    def plotTrayectoria(self):
        """
        >>> from shapely.geometry import Point
        >>> d = {'instante': [1, 2,4],'punto':[Point(1,5),Point(3,3),Point(2,1)],'metros':[30,65,76],'velocidad':[1.3,2.0,7.4], 'estado': [True, True, False]}
        >>> df = gpd.GeoDataFrame(data=d)        
        >>> t=Trayectoria(1,1,df) 
        >>> t.plotTrayectoria()
        """
        #cosa=self.GeoDataFrame[self.GeoDataFrame['estado'] == True]
        plt=self.GeoDataFrame[self.GeoDataFrame['estado'] == 0].plot(figsize=(20, 15),marker='*', color='red', markersize=5)
        self.GeoDataFrame[self.GeoDataFrame['estado'] == 2].plot(figsize=(20, 15),ax=plt,marker='*', color='blue', markersize=5)
        self.GeoDataFrame[self.GeoDataFrame['estado'] == 1].plot(figsize=(20, 15),ax=plt,marker='*', color='green', markersize=5)

        return plt
    def __ObtenerParadas(self,gdf: gpd.GeoDataFrame):
        ruta=list()
        ruta.append(0)
        for i in range(1,len(gdf)):
            if len(ruta)>1 and gdf.loc[ruta[1]:i,'intervalo'].sum()>self.T0:
                for j in ruta:
                    c1=self.__dis([gdf['mX'].iloc[i],gdf['mX'].iloc[j]])
                    c2=self.__dis([gdf['mY'].iloc[i],gdf['mY'].iloc[j]])
                    if np.sqrt(c2**2+c1**2)<self.D0:
                        if j==ruta[len(ruta)-1]:
                            gdf.loc[ruta[0]:i+1,'estado']=1
                            ruta=list()
                            break
                    elif np.sqrt(c2**2+c1**2)>self.D1:
                        gdf.loc[ruta[1]:i,'estado']=0
                        ruta=list()
                        
                        break
            ruta.append(i)
                
        return gdf
    def __dis(self,x):
        return abs(x[0]-x[1])
    def getGDF(self):
        return self.GeoDataFrame
    def getCrs(self):
        return self.crs
    def velocidadMediaParado(self):
        return self.GeoDataFrame.velocidad[self.GeoDataFrame['estado'] == 1].mean()
    def velocidadMediaMovimiento(self):
        return self.GeoDataFrame.velocidad[self.GeoDataFrame['estado'] == 0].mean()
    def velocidadMediaSinDefinir(self):
        return self.GeoDataFrame.velocidad[self.GeoDataFrame['estado'] == 2].mean()
    
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)