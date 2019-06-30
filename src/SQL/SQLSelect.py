# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 21:52:39 2019

@author: Hector
"""
from sqlalchemy.orm import sessionmaker
if __name__ != "__main__":
    from . import SQLConexion as cx
import modelo.TrayectoriaConceptual as tc
import modelo.Trayectoria as tr
import geopandas as gpd
import pandas as pd

def cargarTrayectoriasBrutas(From="From public.punto",Where=""):
    listaTB=list()
    sql="SELECT public.punto.punto, public.punto.instante, public.punto.estado, public.punto.id_trayectoria, public.trayectoria.id_usuario "+From+" INNER JOIN public.trayectoria ON public.punto.id_trayectoria = public.trayectoria.id_trayectoria "+Where+" order by public.punto.id_trayectoria, public.punto.id_punto;"
    if True:
        engine=cx.conexionBDApp()
        Session = sessionmaker(bind=engine)
        session = Session()
        
        datos=gpd.GeoDataFrame.from_postgis(sql, engine, geom_col='punto', crs='epsg:4326', hex_encoded=True, index_col=None, coerce_float=True, params=None)
        session.close()
        maxi=datos.id_trayectoria.max()
        while True:
            
            listaTB.append(tr.Trayectoria(datos[datos.id_trayectoria==datos.id_trayectoria.iloc[0]]))
            if datos.iat[0,3]==maxi:
                break
            datos=datos[datos.id_trayectoria!=datos.id_trayectoria.iloc[0]]
#    except:
#        return -1
    return listaTB


def cargarTrayectoriasConceptuales(From="From public.parado",Where=""):
    """
    >>> cargarTodasLasTrayectoriasConceptuales()
    
    """
    
    listaTC=list()
    sql="SELECT public.parado.punto, public.parado.instante_inicio, public.parado.instante_fin, public.parado.id_parada, public.parado.id_trayectoria, public.trayectoria.id_usuario, public.parado.id_osm "+From+" INNER JOIN public.trayectoria ON public.parado.id_trayectoria = public.trayectoria.id_trayectoria "+Where+" order by public.parado.id_trayectoria, public.parado.id_parada;"
    print(sql)
    if True:
        engine=cx.conexionBDApp()
        Session = sessionmaker(bind=engine)
        session = Session()
        datos=gpd.GeoDataFrame.from_postgis(sql, engine, geom_col='punto', crs='epsg:4326', hex_encoded=True, index_col=None, coerce_float=True, params=None)
        session.close()
        maxi=datos.id_trayectoria.max()
        if len(datos)>0:
            while True:
                if len(datos)>0:
                    a=tc.TrayectoriaConceptual(datos[datos.id_trayectoria==datos.id_trayectoria.iloc[0]])
                    listaTC.append(a)
                    if datos.iat[0,4]==maxi:
                        break
                    datos=datos[datos.id_trayectoria!=datos.id_trayectoria.iloc[0]]
#    except:
#        return -1
    return listaTC
def selectApp(sql):
    try:
        engine=cx.conexionBDApp()
        Session = sessionmaker(bind=engine)
        session = Session()
        df = pd.read_sql_query(sql, engine)
        session.close()
    except:
        return -1
    return df
def selectOSM(sql):
    engine=cx.conexionBDOSM()
    Session = sessionmaker(bind=engine)
    session = Session()
    df = pd.read_sql_query(sql, engine)
    session.close()
    return df

def selectGDF(sql):
    try:
        engine=cx.conexionBDApp()
        Session = sessionmaker(bind=engine)
        session = Session()
        datos=gpd.GeoDataFrame.from_postgis(sql, engine, geom_col='punto', crs='epsg:4326', hex_encoded=True, index_col=None, coerce_float=True, params=None)
        session.close()
        datos['longitud']=datos['punto'].x
        datos['latitud']=datos['punto'].y
        datos=datos.drop(['punto'], axis=1)
    except:
        return -1
        
    return datos
if __name__ == "__main__":
    import SQLConexion as cx
    import doctest
    cargarTrayectoriasConceptuales()    
    
    #doctest.testmod(verbose=False)