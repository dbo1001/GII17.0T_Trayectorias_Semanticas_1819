# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 12:45:50 2019

@author: Hector
"""

from modelo.Trayectoria import Trayectoria
#import geopandas as gpd
from shapely.geometry import Point
class CrearTrayectoria():
    def __init__(self,args=()):
        
        self.gdf=args[0]
        self.idUsu=args[1]
        self.t=args[2]
        self.p=args[3]
        self.m=args[4]
        self.v=args[5]

              
    def run(self):
        #Tiempo para Velocidad
        t=0
        #Colas para obtener la media movil
        from collections import deque
        colaM1=deque()
        colaM23=deque()
        #tuplas de la media y para en intercambio de colas
        tp=tuple()
        mediaX=0
        mediaY=0
        #Parado
        self.gdf['parado']=False
        #DIVIDIR En TRAYECTORIAS
        corte=0
        #RETURN
        r=list()
        conta=0
        for indice,fila in self.gdf.iterrows():
            #########################################################
            #                      VELOCIDAD                        #
            #########################################################
            if conta!=0:
                fila2=self.gdf.iloc[conta-1]
                t=fila[self.t]-fila2[self.t]
                t=t.total_seconds()
                self.gdf.iat[conta,3]=self.__velocidadTramo(fila[self.m],fila2[self.m],t)
                
            #########################################################
            #                      MEDIA MOVIL                      #
            #########################################################
            
            colaM1.appendleft((fila[self.p],fila[self.t]))
            while len(colaM1)!=0 and (fila[self.t]-colaM1[-1][1]).total_seconds()> 60:
                tp=colaM1.popleft()
                if len(colaM23)==0:
                    mediaX=tp[0].x
                    mediaY=tp[0].y
                    colaM23.appendleft(tp)
                else:
                    mediaX=mediaX+(tp[0].x/len(colaM23))
                    mediaY=mediaY+(tp[0].y/len(colaM23))
                    colaM23.appendleft(tp)
            while len(colaM23)!=0 and (fila[self.t]-colaM23[-1][1]).total_seconds()> 180:
                tp=colaM23.popleft()
                mediaX=mediaX-(tp[0].x/(len(colaM23)+1))
                mediaY=mediaY-(tp[0].y/(len(colaM23)+1))
                
            #########################################################
            #                     ¿ESTA PARADO?                     #
            #########################################################
            if(Point(mediaX,mediaY).distance(fila[self.p])<30 or (fila[self.v]<0.6)):
                fila['parado']=True
            #########################################################
            #                       Cortar                          #
            #########################################################
            if t>180 and (fila[self.m].distance(fila2[self.m])>110):
                if conta-corte>5 and (self.gdf.iat[conta,self.t]-self.gdf.iat[corte,self.t]).total_seconds()> 300:
                    r.append(Trayectoria(0,0,self.gdf.iloc[corte:conta]))
                corte=conta
            conta=conta+1
        return r

    def __velocidadTramo(self,p1,p2,t):
        v=p1.distance(p2)
        if t==0:
            t=1
        v=v/t
        return v
    def __paradoVelocidad(self,v):
        if v<0.6:
            return True
        return False

    
    