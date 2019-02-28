# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 12:45:50 2019

@author: Hector
"""

from modelo.Trayectoria import Trayectoria
import numpy as np

import pandas as pd
from shapely.geometry import Point
class CrearTrayectoriaB():
    def __init__(self,args=()):
        
        self.gdf=args[0]
        self.idUsu=args[1]
        self.t=args[2]
        self.p=args[3]
        self.m=args[4]
        self.v=args[5]
        self.D0=43
        self.D1=45
        self.T0=60
              
    def run(self):
        r=list()
        corte=0
        self.gdf['velocidad']=self.gdf.metros.apply(lambda x: x.y)
        self.gdf['mY']=self.gdf.metros.apply(lambda x: x.y)
        self.gdf['mX']=self.gdf.metros.apply(lambda x: x.x)
        self.gdf['metros']=self.gdf.metros.apply(lambda x: x.x)
        self.gdf['metros']=self.gdf.metros.rolling(2).apply(self.__dis,raw=True)
        self.gdf['velocidad']=self.gdf.velocidad.rolling(2).apply(self.__dis,raw=True)
        self.gdf['metros']=self.gdf.apply(lambda x: (np.sqrt(x['velocidad']**2+x['metros']**2)),axis=1)
        self.gdf['velocidad']=pd.to_timedelta(self.gdf['time']).dt.total_seconds()
        self.gdf['intervalo']=self.gdf.velocidad.rolling(2).apply(lambda x: (x[1]-x[0]),raw=True)
        self.gdf['velocidad']=self.gdf.apply(lambda x: (x['metros']/x['intervalo']),axis=1)
        #valore para parado 0 movimiento, 1 parado, 2 no se sabe
        self.gdf['parado']=2
        self.gdf=self.gdf.reset_index()
        
        #########################################
        #                PARADO                 #
        #########################################
        ruta=list()
        ruta.append(0)
        for i in range(1,len(self.gdf)):
            corta=self.__disParada(i,ruta)
            if corta:
                ruta=list()
            ruta.append(i)
                
        
        
        for i in range(1,len(self.gdf)):
            if self.gdf.iat[i,7]>180 and (self.gdf.iat[i,3]>110):
                if i-corte>5 and self.gdf.iat[i,7]> 300:
                    r.append(Trayectoria(0,0,self.gdf.iloc[corte:i]))
                corte=i

        return r
    def __dis(self,x):
        return abs(x[0]-x[1])
    def __disParada(self,i,ruta):
        if self.gdf.loc[ruta[0]:i,'intervalo'].sum()>self.T0:
            for j in ruta:
                c1=self.__dis([self.gdf['mX'].iloc[i],self.gdf['mX'].iloc[j]])
                c2=self.__dis([self.gdf['mY'].iloc[i],self.gdf['mY'].iloc[j]])
                if np.sqrt(c2**2+c1**2)<self.D0:
                    self.gdf.loc[ruta[0]:i,'parado']=1
                elif np.sqrt(c2**2+c1**2)>self.D1:
                    self.gdf.loc[ruta[0]:i,'parado']=0
                return True
        return False
#    def __disParada(self,i,ruta):
#        
#        for j in ruta:
#            c1=self.__dis([self.gdf['mX'].iloc[i],self.gdf['mX'].iloc[j]])
#            c2=self.__dis([self.gdf['mY'].iloc[i],self.gdf['mY'].iloc[j]])
#            if not( np.sqrt(c2**2+c1**2)<self.D0):
#                if  np.sqrt(c2**2+c1**2)>self.D1:
#                    self.gdf.loc[ruta[0]:i,'parado']=0
#                else:
#                    if self.gdf.loc[ruta[0]:i,'intervalo'].sum()>self.T0:
#                        self.gdf.loc[ruta[0]:i,'parado']=1
#                return True
#        return False
            