# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 17:31:14 2019

@author: Hector
"""
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from .ConfiguracionDeLectura import ConfiguracionDeLectura as CDL

#from ..trayectoria import Trayectoria

class LoadCSV():
    def __init__(self,cdl: CDL):
        self.CDL=cdl
        pass
        
    def __leerArchivo(self,route):
        usar=list()
        formFecha=""
        usar.append(self.CDL.x)
        usar.append(self.CDL.y)
        for i,j in enumerate(self.CDL.t):
            usar.append(j)
            formFecha=formFecha+self.CDL.ts[i]
        data= pd.read_csv(route, error_bad_lines=False,header=None,skiprows=self.CDL.lineaIni,usecols=usar)
        if len(self.CDL.t)>1:
            for i in range(1,len(self.CDL.t)):
                data[usar[2]] = data[usar[2]] + data[usar[i+2]]
                data=data.drop(usar[i+2],1)
        data[usar[2]]=pd.to_datetime(data[usar[2]],format=formFecha)
        data=data.rename(columns={usar[2]: 'instante'})
        self.t='instante'
        return data
    
    def rutasPorUsuario(self,ruta):
        import os
        gdf=pd.DataFrame()
        rutaAnterior=""
        for i in self.burcarFicheros(ruta):
            if os.path.dirname(i)==rutaAnterior or rutaAnterior=="":
                os.path.isfile(i)
                gdf=pd.concat([gdf,self.__leerArchivo(i)])
            else:
                gdf=self.__comvertirEnGEO(gdf)
                yield gdf
                gdf=self.__leerArchivo(i)
            rutaAnterior=os.path.dirname(i)
        gdf=self.__comvertirEnGEO(gdf)
        
        yield gdf
        
    def burcarFicheros(self,route):
        import os
        rootDir = route
        for dirName, subdirList, fileList in os.walk(rootDir):
            for fname in fileList:
                if fname[len(fname)-(len(self.CDL.extension)):len(fname)]==self.CDL.extension:
                    complet=dirName+'/'+fname
                    aux=""
                    for j in complet:
                        if j=='\\':
                            aux=aux+"/"
                        else:
                            aux=aux+j
                    yield aux
    def crearTrayectoria(self,df):
        
        return self.__dividirTrayectoria(df)
        
        pass
    def __dividirTrayectoria(self,df: gpd.GeoDataFrame):
        from .CrearTrayectoria import CrearTrayectoria
        
        r=list()
        hiloCrearTrayectoria=CrearTrayectoria(args=[df,0,0,1,2,3,r])
        hiloCrearTrayectoria.start()
        hiloCrearTrayectoria.join()
        return r
    
    def __comvertirEnGEO(self,dFrame):
        dFrame['punto']=list(zip(dFrame[self.CDL.x], dFrame[self.CDL.y]))
        dFrame['punto'] = dFrame['punto'].apply(Point)
        geoFrame = gpd.GeoDataFrame(dFrame, geometry='punto')
        geoFrame=geoFrame.drop(self.CDL.x,1)
        geoFrame=geoFrame.drop(self.CDL.y,1)
        return geoFrame            
        
        
    
