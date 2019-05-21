# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 16:12:10 2019

@author: Hector
"""

from . import SQLConexion as cx

from sqlalchemy.orm import sessionmaker

#https://sphinxcontrib-napoleon.readthedocs.io/en/latest/
def updateIdOSM(datos):
    """
    Summary line.
    
    Actualiza la id de osm que hay en la tabla parado
    
    Parameters
    ----------
    datos : [id_parada,id_osm]
        Primera columna id de paradas, seguda columna id del punto mas cercano de OSM
    
    Returns
    -------
    int
        0 -> Update correcto
        -1 -> Fallo en el Update
    
    """
    try:
        engine=cx.conexionBDApp()
        Session = sessionmaker(bind=engine)
        session = Session()
        for i in datos:
            engine.execute('UPDATE parado SET id_osm='+str(i[2])+' WHERE id_parada = '+str(i[0])+' AND id_trayectoria='+str(i[1]))
        session.close()
    except:
        return -1
    return 0