# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 18:57:38 2019

@author: Hector
"""

def conexionBDApp():
    from sqlalchemy import create_engine,MetaData,func
    from sqlalchemy.orm import sessionmaker
    
    usuario = "postgres"
    contrasena="123456"
    ip="localhost"
    puerto="5432"
    db="DB_Trayectorias_Semanticas"
    
    engine = create_engine('postgresql://'+usuario+':'+contrasena+'@'+ip+':'+puerto+'/'+db, echo=False) 
    return engine

def conexionBDOSM():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    usuario = "postgres"
    contrasena="123456"
    ip="localhost"
    puerto="5432"
    db="OSMSpain"
    
    engine = create_engine('postgresql://'+usuario+':'+contrasena+'@'+ip+':'+puerto+'/'+db, echo=False) 
    return engine




    Session = sessionmaker(bind=engine)
    session = Session()
    resul=engine.execute('SELECT max(id_trayectoria) from trayectoria')
    session.close()
    print(resul.fetchone()[0])
conexionBDOSM()    