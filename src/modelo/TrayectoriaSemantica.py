# -*- coding: utf-8 -*-
"""
Created on Sun May  5 17:38:21 2019

@author: Hector
"""
from . import TrayectoriaConceptual
from nominatim import peticion as pet
import pandas as pd
class TrayectoriasSemantica():
    def __init__(self,trayectoria,tParadas=600):
        self.__tParadas=tParadas
        if isinstance(trayectoria,TrayectoriaConceptual.TrayectoriaConceptual):
            self.__idTrayectoria=trayectoria.getIdTrayectoria()
            self.__idUsuario=trayectoria.getIdUsuario()
            self.__gdf=pd.DataFrame(columns=['id_osm','instante_inicio','instante_fin'])
            self.__crearTrayectoriaSemantica(trayectoria.getGDF().copy())
        elif isinstance(trayectoria,pd.DataFrame):
            self.__idTrayectoria=trayectoria.id_trayectoria.iloc[0]
            self.__idUsuario=trayectoria.id_usuario.iloc[0]
            self.__gdf=trayectoria[['id_osm',"instante_inicio","instante_fin"]]
        else:
            self.__idTrayectoria=None
            self.__idUsuario=None
            self.__gdf=None
        
    pass
    def __crearTrayectoriaSemantica(self,gdf):
        ultimo=-1
        for i in range(len(gdf)):

            json=pet.getNominatimforId(gdf.id_osm.iloc[i])
            if json!=-1 and not(json is None):
                if json['features'][0]['properties']['osm_id']!=ultimo:
                    self.__gdf.loc[len(self.__gdf)]=[json['features'][0]['properties']['osm_id'],gdf["instante_inicio"].iloc[i],gdf["instante_fin"].iloc[i]]
                    ultimo=json['features'][0]['properties']['osm_id']
                else:
                    self.__gdf.instante_fin.iloc[len(self.__gdf)-1]=gdf["instante_fin"].iloc[i]
        self.__gdf['tiempo']=pd.to_timedelta(self.__gdf['instante_fin']).dt.total_seconds()
        self.__gdf['tiempo']=self.__gdf['tiempo']-pd.to_timedelta(self.__gdf['instante_inicio']).dt.total_seconds()
        self.__gdf=self.__gdf[self.__gdf['tiempo']>self.__tParadas]
        self.__gdf=self.__gdf[['id_osm','instante_inicio','instante_fin']]
        pass
    def getDF(self):
        return self.__gdf
    def getListOSMId(self):
        return self.__gdf.id_osm.tolist()
        