# -*- coding: utf-8 -*-
"""
Created on Wed May 22 01:40:06 2019

@author: Hector
"""
from modelo import TrayectoriaSemantica 
class Conversor():
    def __init__(self):
        pass
    def TStoIdOSM(self,lts):
        lista=list()
        for ts in lts:
            if len(ts.getListOSMId())>2:
                lista.append(ts.getListOSMId())
        return lista
    def TCtoTS(self,ltc,tParadas=600):
        lts=list()
        for i in ltc:
            lts.append(TrayectoriaSemantica.TrayectoriasSemantica(i,tParadas=tParadas))
        return lts
            