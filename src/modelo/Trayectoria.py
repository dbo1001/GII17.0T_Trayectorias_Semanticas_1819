# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 18:45:50 2019

@author: Hector
"""
import geopandas as gpd
class Trayectoria():
    def __init__(self,idr,idu,gdf: gpd.GeoDataFrame):
        self.idRuta=idr
        self.idUsuario=idu
        self.GeoDataFrame=gdf
        pass
    def __str__(self):
        return(str(self.GeoDataFrame))
