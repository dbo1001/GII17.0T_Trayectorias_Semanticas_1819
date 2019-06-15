# -*- coding: utf-8 -*-
"""
Created on Fri May 24 19:43:17 2019

@author: Hector
"""
from wtforms import Form
from wtforms import StringField,IntegerField
from flask_wtf.file import FileField

class FormularioCargar(Form):
    ruta=FileField(label="Ruta de los archivos:",id="upload")
    longitud=IntegerField(label="Columna de la longitud:")
    latitud=IntegerField(label="Columna de la latitud:")
    lineainicio=IntegerField(label="Fila de inicio de los datos:")
    columnaUsuario=IntegerField(label="Columna del usuario:")
    columnaTiempo1=IntegerField(label="Columna de tiempo 1:")
    columnaTiempo2=IntegerField(label="Columna de tiempo 2:")
    formatoTiempo1=StringField(label="Formato del tiempo 1:")
    formatoTiempo2=StringField(label="Formato del tiempo 2:")
    extension=StringField(label="Extensión de los archivos:")
    
    pass