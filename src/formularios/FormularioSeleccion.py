# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 18:24:52 2019

@author: Hector
"""

from wtforms import Form
from wtforms import StringField,IntegerField, SelectField,TextAreaField

class FormularioSeleccion(Form):
    usuario=IntegerField(label="Usuario:",id="user")
    dia=SelectField('Programming Language',choices=[('cpp', 'Lunes'), ('py', 'Martes'), ('text', 'Miércoles'),('','Jueves'),('','Viernes'),('','Miércoles'),('','Sábado'),('','Domingo')],id="day")
    
    select="SELECT public.parado.punto, public.parado.instante_inicio, public.parado.instante_fin, public.parado.id_parada, public.parado.id_trayectoria, public.trayectoria.id_usuario, public.parado.id_osm "
    tFrom=" FROM public.parado "
    taFrom=TextAreaField(select+'<br/>'+tFrom)
    tWhere=" INNER JOIN public.trayectoria ON public.parado.id_trayectoria = public.trayectoria.id_trayectoria "
    taWhere=TextAreaField(tWhere)
    sWhere=StringField()
    tOrder=" ORDER BY public.parado.id_trayectoria, public.parado.id_parada;"