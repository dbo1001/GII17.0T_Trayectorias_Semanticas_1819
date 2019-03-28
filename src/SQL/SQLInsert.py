# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 22:06:11 2019

@author: Hector
"""
from . import SQLConexion as cx
from geoalchemy2 import Geometry, WKTElement
from sqlalchemy.orm import sessionmaker
def insertUsuarios(usuarios: list):
    try:
        engine=cx.conexionBDApp()
        Session = sessionmaker(bind=engine)
        session = Session()
        for i in usuarios:
            engine.execute('INSERT INTO usuario (id_usuario) VALUES ('+str(i)+')')
        session.close()
    except:
        return -1
    return 0
def insertTrayectoria(trayectorias: list):
    try:
        engine=cx.conexionBDApp()
        Session = sessionmaker(bind=engine)
        session = Session()
        for i in trayectorias:
            engine.execute('INSERT INTO trayectoria(id_usuario, id_trayectoria) VALUES ('+str(i.getIdUsuario())+','+str(i.getIdRuta())+')')
            gdf=i.getGDF().copy()
            gdf=gdf[["punto","instante","estado"]]
            gdf["id_trayectoria"]=int(i.getIdRuta())
            gdf["id_punto"]=gdf.index
            gdf['punto']=gdf['punto'].apply(lambda x: WKTElement(x.wkt, srid=4326))
            gdf.to_sql("punto", engine, if_exists='append', index=False,dtype={'punto': Geometry('POINT',srid=4326)})
        session.close()
    except:
        return -1
    return 0
def insertarTrayectoriaConceptual(trayectorias: list):
    if True:
        engine=cx.conexionBDApp()
        Session = sessionmaker(bind=engine)
        session = Session()
        for i in trayectorias:
            gdf=i.getGDF().copy()
            gdf["id_trayectoria"]=int(i.getIdTrayectoria())
            gdf["id_parada"]=gdf.index
            gdf['punto']=gdf['punto'].apply(lambda x: WKTElement(x.wkt, srid=4326))
            gdf.to_sql("parado", engine, if_exists='append', index=False,dtype={'punto': Geometry('POINT',srid=4326)})
        session.close()

    return 0