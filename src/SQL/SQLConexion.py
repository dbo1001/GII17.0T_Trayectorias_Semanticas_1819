# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 18:57:38 2019

@author: Hector
"""

def conexionBDApp():
    from sqlalchemy import create_engine

    
    usuario = "postgres"
    contrasena="123456"
    ip="localhost"
    puerto="5432"
    db="DB_Trayectorias_Semanticas"
    
    engine = create_engine('postgresql://'+usuario+':'+contrasena+'@'+ip+':'+puerto+'/'+db, echo=False) 
    return engine
