# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 20:34:28 2019

@author: Hector
"""
from modelo.Trayectoria import Trayectoria
class Estadisticas():
    def porcentajeDeParadas(self,lgdf: list([Trayectoria])):
        """
        >>> from Trayectoria import Trayectoria
        >>> import geopandas as gpd
        >>> from shapely.geometry import Point
        >>> d = {'time': [1, 2,4],'punto':[Point(1,5),Point(3,3),Point(2,1)],'metros':[30,65,76],'velocidad':[1.3,2.0,7.4], 'parado': [True, True, False]}
        >>> df = gpd.GeoDataFrame(data=d)        
        >>> t=Trayectoria(1,1,df)
        >>> l=[t,t,t]
        >>> est=Estadisticas()
        >>> est.porcentajeDeParadas(l)
        66.66666666666666
        """
        tam = 0
        par = 0
        for i in lgdf:
            par+=i.numParados()
            tam+=i.getNumElementos()
        return (par/tam)*100

    def plotTrayectorias(self,l):
        """
        >>> from shapely.geometry import Point
        >>> d = {'time': [1, 2,4],'punto':[Point(1,5),Point(3,3),Point(2,1)],'metros':[30,65,76],'velocidad':[1.3,2.0,7.4], 'parado': [True, True, False]}
        >>> df = gpd.GeoDataFrame(data=d)        
        >>> t=Trayectoria(1,1,df) 
        >>> t.plotTrayectoria()
        """

        p=l[0].getGDF()[l[0].getGDF()['parado'] == 1].plot(marker='*', color='green', markersize=5)
        for i in l:
            p=i.getGDF()[i.getGDF()['parado'] == 1].plot(figsize=(20, 15),marker='*', color='green', markersize=5)
            p=i.getGDF()[i.getGDF()['parado'] == 0].plot(figsize=(20, 15),ax=p,marker='*', color='red', markersize=5)
            p=i.getGDF()[i.getGDF()['parado'] == 2].plot(figsize=(20, 15),ax=p,marker='*', color='blue', markersize=5)
        pass

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)