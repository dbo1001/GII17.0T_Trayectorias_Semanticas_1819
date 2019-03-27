# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 12:45:50 2019

@author: Hector
"""

from modelo.Trayectoria import Trayectoria
import numpy as np
import pandas as pd
from .ConfiguracionDeLectura import ConfiguracionDeLectura as CDL
class CrearTrayectoriaB():
    def __init__(self,args=()):
        
        self.gdf=args[0]
        self.idUsu=args[1]
        self.t=args[2]
        self.p=args[3]
        self.m=args[4]
        self.v=args[5]
        self.D0=35
        self.D1=45
        self.T0=60
        self.CDL=CDL()
              
    def run(self):
        r=list()
        corte=0
        self.gdf["estado"]=2
        print(list(self.gdf.columns))
        self.CalcularDatos(self.gdf,self.CDL.crs)
        print(list(self.gdf.columns))
        #########################################
        #                Dividir                #
        #########################################
                        
        
        for i in range(1,len(self.gdf)):
            if self.gdf.iat[i,7]>180 and (self.gdf.iat[i,3]>110):
                if i-corte>15 and abs(self.gdf.iloc[corte:i].intervalo.sum())> 300:
                    r.append(Trayectoria(0,0,self.gdf.iloc[corte:i].copy()))
                corte=i
        
        return r
    def CalcularDatos(self, gdf,crs):
        df1=gdf['punto'].copy()
        df1.crs={'init': crs, 'no_defs': True}
        df1=df1.to_crs(epsg=3395)
        gdf['metros']=df1
        gdf['velocidad']=0.0
        gdf['velocidad']=gdf.metros.apply(lambda x: x.y)
        gdf['mY']=gdf.metros.apply(lambda x: x.y)
        gdf['mX']=gdf.metros.apply(lambda x: x.x)
        gdf['metros']=gdf.metros.apply(lambda x: x.x)
        gdf['metros']=gdf.metros.rolling(2).apply(self.__dis,raw=True)
        gdf['velocidad']=gdf.velocidad.rolling(2).apply(self.__dis,raw=True)
        gdf['metros']=gdf.apply(lambda x: (np.sqrt(x['velocidad']**2+x['metros']**2)),axis=1)
        gdf['velocidad']=pd.to_timedelta(gdf['time']).dt.total_seconds()
        gdf['intervalo']=gdf.velocidad.rolling(2).apply(lambda x: abs(x[1]-x[0]),raw=True)
        gdf['velocidad']=gdf.apply(lambda x: (x['metros']/x['intervalo']),axis=1)
        #valore para parado 0 movimiento, 1 parado, 2 no se sabe
        gdf=gdf.reset_index(drop=True)
        return gdf
    def __dis(self,x):
        return abs(x[0]-x[1])

            