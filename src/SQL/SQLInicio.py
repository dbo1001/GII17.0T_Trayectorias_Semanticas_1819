# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 20:20:15 2019

@author: Hector
"""
from . import SQLConexion as cx
from sqlalchemy.orm import sessionmaker
def idUsuario():
    engine=cx.conexionBDApp()
    Session = sessionmaker(bind=engine)
    session = Session()
    resul=engine.execute('SELECT max(id_usuario) from usuario')
    session.close()
    r=resul.fetchone()[0]
    if r==None:
        return -1
    return r


def idTrayectoria():
    engine=cx.conexionBDApp()
    Session = sessionmaker(bind=engine)
    session = Session()
    resul=engine.execute('SELECT max(id_trayectoria) from trayectoria')
    session.close()
    r=resul.fetchone()[0]
    if r==None:
        return -1
    return r

    