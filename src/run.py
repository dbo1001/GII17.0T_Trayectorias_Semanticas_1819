# -*- coding: utf-8 -*-
"""
Created on Wed May 22 00:18:19 2019

@author: Hector
"""

from flask import Flask
from flask import render_template
from formularios import FormularioCargar
app=Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/Cargar")
def cargar():
    form=FormularioCargar.FormularioCargar()
    return render_template('cargar.html', form=form)
@app.route("/Prediccion")
def prediccion():
    return render_template('prediccion.html')
@app.route("/Clustering")
def clustering():
    return render_template('clustering.html')

if __name__=="__main__":
    app.run(port=8000,debug=True)