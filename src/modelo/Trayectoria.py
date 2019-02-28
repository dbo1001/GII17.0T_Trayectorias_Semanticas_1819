# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 18:45:50 2019

@author: Hector
"""
import geoplot
import geopandas as gpd
class Trayectoria():
    def __init__(self,idr,idu,gdf: gpd.GeoDataFrame):
        self.idRuta=idr
        self.idUsuario=idu
        self.GeoDataFrame=gdf
        pass
    def __str__(self):
        return(str(self.GeoDataFrame['parado']))
    def getNumElementos(self):
        """
        >>> from shapely.geometry import Point
        >>> d = {'time': [1, 2,4],'punto':[Point(1,5),Point(3,3),Point(2,1)],'metros':[30,65,76],'velocidad':[1.3,2.0,7.4], 'parado': [True, True, False]}
        >>> df = gpd.GeoDataFrame(data=d)        
        >>> t=Trayectoria(1,1,df)        
        >>> t.getNumElementos()
        3
        """
        return self.GeoDataFrame.shape[0]
    
    def getIdUsuario(self):
        """
        >>> from shapely.geometry import Point
        >>> d = {'time': [1, 2,4],'punto':[Point(1,5),Point(3,3),Point(2,1)],'metros':[30,65,76],'velocidad':[1.3,2.0,7.4], 'parado': [True, True, False]}
        >>> df = gpd.GeoDataFrame(data=d)        
        >>> t=Trayectoria(1,1,df) 
        >>> t.getIdUsuario()
        1
        """
        return self.idUsuario
    
    def getIdRuta(self):
        """
        >>> from shapely.geometry import Point
        >>> d = {'time': [1, 2,4],'punto':[Point(1,5),Point(3,3),Point(2,1)],'metros':[30,65,76],'velocidad':[1.3,2.0,7.4], 'parado': [True, True, False]}
        >>> df = gpd.GeoDataFrame(data=d)        
        >>> t=Trayectoria(1,1,df) 
        >>> t.getIdRuta()
        1
        """
        return self.idRuta
    
    def numParados(self):
        """
        >>> from shapely.geometry import Point
        >>> d = {'time': [1, 2,4],'punto':[Point(1,5),Point(3,3),Point(2,1)],'metros':[30,65,76],'velocidad':[1.3,2.0,7.4], 'parado': [True, True, False]}
        >>> df = gpd.GeoDataFrame(data=d)        
        >>> t=Trayectoria(1,1,df) 
        >>> t.numParados()
        2
        """
        try:
            r=self.GeoDataFrame['parado'].value_counts()[1]
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
        >>> d = {'time': [1, 2,4],'punto':[Point(1,5),Point(3,3),Point(2,1)],'metros':[30,65,76],'velocidad':[1.3,2.0,7.4], 'parado': [True, True, False]}
        >>> df = gpd.GeoDataFrame(data=d)        
        >>> t=Trayectoria(1,1,df) 
        >>> t.plotTrayectoria()
        """
        #cosa=self.GeoDataFrame[self.GeoDataFrame['parado'] == True]

        plt=self.GeoDataFrame[self.GeoDataFrame['parado'] == 1].plot(figsize=(20, 15),marker='*', color='green', markersize=5)
        self.GeoDataFrame[self.GeoDataFrame['parado'] == 0].plot(figsize=(20, 15),ax=plt,marker='*', color='red', markersize=5)
        self.GeoDataFrame[self.GeoDataFrame['parado'] == 2].plot(figsize=(20, 15),ax=plt,marker='*', color='blue', markersize=5)
        return plt
        
    def getGDF(self):
        return self.GeoDataFrame
    def velocidadMediaParado(self):
        return self.GeoDataFrame.velocidad[self.GeoDataFrame['parado'] == 1].mean()
    def velocidadMediaMovimiento(self):
        return self.GeoDataFrame.velocidad[self.GeoDataFrame['parado'] == 0].mean()
    def velocidadMediaSinDefinir(self):
        return self.GeoDataFrame.velocidad[self.GeoDataFrame['parado'] == 2].mean()
    
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)