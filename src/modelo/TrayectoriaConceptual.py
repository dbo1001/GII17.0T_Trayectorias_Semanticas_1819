# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 17:31:39 2019

@author: Hector
"""
#import math
from shapely.geometry import  Point
#from shapely.geometry import LineString
import geopandas as gpd
class TrayectoriaConceptual():
    def __init__(self,trayectoria):
        self.gdf=gpd.GeoDataFrame(columns=['punto','instante_inicio','instante_fin'],geometry="punto")
        self.__CombertirAConceptual(trayectoria)
        self.__idTrayectoria=trayectoria.getIdRuta()
        pass
#    def __CombertirAConceptual(self,trayectoria):
#        gdf=trayectoria.GeoDataFrame
#        parado=list()
#        movimiento=list()
#        if gdf.estado[0]==1:
#            parado.append(0)
#        else:
#            movimiento.append(0)
#        for i in range(1,len(gdf)):
#            if gdf.estado[i]==1:
#                if len(parado)==0:
#                    self.crearSegmento(movimiento,gdf)
#                    movimiento=list()
#                parado.append(i)
#            else:
#                if len(movimiento)==0:
#                    self.crearParada(parado,gdf)
#                    parado=list()
#                movimiento.append(i)  
#        plt=self.gdf.plot(figsize=(20, 15), color='red', markersize=5)
#        
#        pass
    def __CombertirAConceptual(self,trayectoria):
        gdf=trayectoria.GeoDataFrame
        parado=list()
        for i in range(len(gdf)):
            if gdf.estado[i]==1:
                parado.append(i)
            elif len(parado)>0:
                self.crearParada(parado,gdf)
                parado=list()
        if len(parado)>0:
            self.crearParada(parado,gdf)
            parado=list()
        plt=gdf.plot(figsize=(20, 15), color='blue', markersize=5)        
        plt=self.gdf.plot(figsize=(20, 15),ax=plt, color='red', markersize=50)
        
        pass
#    def pendiente(self,x1,x2,y1,y2):
#        """
#        1,4,2,1
#        >>> t=TrayectoriaConceptual(" ")
#        >>> t.pendiente(1,4,2,1)
#        -0.3333333333333333
#        
#        """
#        return (y2-y1)/(x2-x1)
#    def angulo(self,m1,m2):
#        """
#        >>> t=TrayectoriaConceptual(" ")
#        >>> t.angulo(2,-2/3)
#        82.87498365109822
#        """
#        return math.degrees(math.atan((m2-m1)/(1+m2*m1)))
#    def crearSegmento(self,lista,gdf):
#        sumT=0
#        if self.gdf.shape[0]==0:
#            ini=lista[0]
#            tIni=gdf.time[ini]
#            pIni=gdf.punto[ini]
#            lista.remove[0]
#        else:
#            ini=self.gdf.index[self.gdf.shape[0]-1]
#            tIni=self.gdf.instante_fin[ini]
#            pIni=self.gdf.geometry[ini]
#        
#        for i in lista:
#            if sumT+gdf.intervalo[i]>60:
#                self.gdf.loc[len(self.gdf)]=[LineString([pIni,gdf.punto[i]]),tIni,gdf.time[i]]
#                sumT=0
#                pIni=gdf.punto[i]
#                tIni=gdf.time[i]
#            else:
#                sumT=sumT+gdf.intervalo[i]
#        if len(gdf)>lista[len(lista)-1]:
#            self.gdf.loc[len(self.gdf)]=[LineString([pIni,gdf.punto[lista[len(lista)-1]+1]]),tIni,gdf.time[lista[len(lista)-1]+1]]   
#        pass

    def crearParada(self,lista,gdf):
        x=0
        y=0
        for i in lista:
           x=x+gdf.punto[i].x
           y=y+gdf.punto[i].y
        p=Point(x/len(lista),y/len(lista))
        self.gdf.loc[len(self.gdf)]=[ p,gdf.instante[lista[0]],gdf.instante[lista[len(lista)-1]]]
        print(len(lista))
        pass
    def getIdTrayectoria(self):
        return self.__idTrayectoria
    def getGDF(self):
        return self.gdf
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)