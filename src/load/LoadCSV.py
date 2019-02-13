# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 17:31:14 2019

@author: Hector
"""
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from modelo.Trayectoria import Trayectoria

#from ..trayectoria import Trayectoria

class LoadCSV():
    def __init__(self,x,y,t,e,crs):
        self.__estension=e
        self.crs=crs
        self.__primeraLinea=0
        self.x=x
        self.y=y
        self.__t=t
        self.t=''
        
    def __leerArchivo(self,route):
        usar=list()
        formFecha=""
        usar.append(self.x)
        usar.append(self.y)
        if type(self.__t)!= tuple:
            for j in self.__t:
                usar.append(j[0])
                formFecha=self.__t[0][1]+' '+self.__t[1][1]
        else:
            usar.append(self.__t[0])
            formFecha=self.__t[1]
        data= pd.read_csv(route, error_bad_lines=False,header=None,skiprows=6,usecols=usar)
        if type(self.__t)!= tuple:
            data[usar[2]] = data[usar[2]] +' '+ data[usar[3]]
            
            data=data.drop(usar[3],1)
        data[usar[2]]=pd.to_datetime(data[usar[2]],format=formFecha)
        data=data.rename(columns={usar[2]: 'time'})
        self.t='time'
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
                df1=gdf['punto'].copy()
                df1.crs={'init': self.crs, 'no_defs': True}
                df1=df1.to_crs(epsg=3395)
                gdf['metros']=df1
                gdf['velocidad']=0.0
                yield gdf
                gdf=self.__leerArchivo(i)
            rutaAnterior=os.path.dirname(i)
        gdf=self.__comvertirEnGEO(gdf)
        df1=gdf['punto'].copy()
        df1.crs={'init': self.crs, 'no_defs': True}
        df1=df1.to_crs(epsg=3395)
        gdf['metros']=df1
        gdf['velocidad']=0.0
        yield gdf
        
    def burcarFicheros(self,route):
        import os
        rootDir = route
        for dirName, subdirList, fileList in os.walk(rootDir):
            for fname in fileList:
                if fname[len(fname)-(len(self.__estension)):len(fname)]==self.__estension:
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
        dFrame['punto']=list(zip(dFrame[self.x], dFrame[self.y]))
        dFrame['punto'] = dFrame['punto'].apply(Point)
        geoFrame = gpd.GeoDataFrame(dFrame, geometry='punto')
        geoFrame=geoFrame.drop(self.x,1)
        geoFrame=geoFrame.drop(self.y,1)
        return geoFrame            
        
        
    
