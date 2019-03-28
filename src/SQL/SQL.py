# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 17:11:05 2019

@author: Hector
"""




from geoalchemy2 import Geometry, WKTElement
from sqlalchemy import create_engine, MetaData
import pandas as pd
import geopandas as gpd
from sqlalchemy.orm import sessionmaker

# Creating SQLAlchemy's engine to use
def guardarRuta(gf,idruta,idusuario,idusuarioruta):
    
    #engine = create_engine('postgresql://username:password@host:socket/database')

    engine = create_engine('postgresql://postgres:123456@localhost:5432/dataSet_China', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    meta = MetaData(engine, schema='esquema')
    gf['punto']=gf['punto'].apply(lambda x: WKTElement(x.wkt, srid=4326))
    
    print(gf['punto'])
    gf.crs={'init': 'epsg:4326'}
    if idusuario!='':
        engine.execute('INSERT INTO usuario (usuario_id) VALUES ('+idusuario+')')
    engine.execute('INSERT INTO ruta (ruta_id, usuario_id) VALUES ('+str(idruta)+', '+idusuarioruta+')')
    gf.to_sql("puntogps", engine, if_exists='append', index=False,dtype={'punto': Geometry('POINT',srid=4326)})
    
    session.close()
def consultaSQL():
    
    pass


    


#drop the geometry column as it is now duplicative
    #geodataframe.drop('geometry', 1, inplace=True)

# Use 'dtype' to specify column's type
# For the geom column, we will use GeoAlchemy's type 'Geometry'
    #geodataframe.to_sql("PuntoGPS", engine, if_exists='append', index=False, 
     #                    dtype={'geom': Geometry('POINT', srid= <your_srid>)})
