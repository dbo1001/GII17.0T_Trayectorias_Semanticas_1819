# -*- coding: utf-8 -*-
"""
Created on Fri May 24 19:43:17 2019

@author: Hector
"""
from wtforms import Form
from wtforms import StringField,IntegerField,validators
from flask_wtf.file import FileField



class FormularioCargar(Form):

 
    ruta=FileField("Ruta de los archivos*",[validators.Required()],id="upload")
    longitud=IntegerField("Columna de la longitud*",[validators.Required()],id="longitud")
    latitud=IntegerField("Columna de la latitud*",[validators.Required()],id="latitud")
    lineainicio=IntegerField("Fila de inicio de los datos*",[validators.Required()],id="lineainicio")
    columnaTiempo1=IntegerField("Columna de tiempo 1*",[validators.Required()],id="columnaTiempo1")
    columnaTiempo2=IntegerField("Columna de tiempo 2",[validators.Required()],id="columnaTiempo2")
    formatoTiempo1=StringField("Formato del tiempo 1*",[validators.Required()],id="formatoTiempo1")
    formatoTiempo2=StringField("Formato del tiempo 2",[validators.Required()],id="formatoTiempo2")
    extension=StringField("Extensión de los archivos*",[validators.Required()],id="extension")


    pass