# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 19:09:06 2019

@author: Hector
"""

class ConfiguracionDeLectura():
    def __init__(self,x=0,y=1,t=list(),ts= list(),extension="",tipo="CSV",crs='epsg:4326',lineaIni=0):
        self.extension=extension
        self.x=x
        self.y=y
        self.t=t
        self.ts=ts 
        self.tipo=tipo
        self.crs=crs
        self.lineaIni=lineaIni
        if tipo=="GPX":
            self.extension=extension
            self.t=(None,"time")
            self.x=("wpt","lon")
            self.y=("wpt","lat")
            self.ts="%Y-%m-%dT%H:%M:%SZ"
