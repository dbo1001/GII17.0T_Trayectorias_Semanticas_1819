# -*- coding: utf-8 -*-
"""
Created on Fri May 24 19:43:17 2019

@author: Hector
"""
from wtforms import Form
from wtforms import StringField,IntegerField
class FormularioCargar(Form):
    ruta=StringField()
    longitud=IntegerField()
    latitud=IntegerField()
    lineainicio=IntegerField()
    columnaUsuario=IntegerField()
    columnaTiempo1=IntegerField()
    columnaTiempo2=IntegerField()
    formatoTiempo1=StringField()
    formatoTiempo2=StringField()
    extension=StringField()
    
    pass