# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 20:40:46 2019

@author: Hector
"""
import SQL.SQLInicio as sqlini
class idTrayectoria():
    def __init__(self):
        try:
            self.id=sqlini.idTrayectoria()
        except:
            print( "ERROR AL CONECTAR CON LA BASE DE DATOS")
    def cId(self):
        self.id=self.id+1
        return self.id
    
class idUsuario():
    def __init__(self):
        try:
            self.id=sqlini.idUsuario()
        except:
            print( "ERROR AL CONECTAR CON LA BASE DE DATOS")
    def cId(self):
        self.id=self.id+1
        return self.id    
    