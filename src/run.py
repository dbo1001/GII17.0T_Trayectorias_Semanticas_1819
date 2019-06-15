# -*- coding: utf-8 -*-
"""
Created on Wed May 22 00:18:19 2019

@author: Hector
"""
import os
from flask import Flask
from flask import render_template,request
from werkzeug import secure_filename
from formularios import FormularioCargar,FormularioSeleccion
app=Flask(__name__)
app.config['UPLOAD_FOLDER']=os.path.dirname(os.path.realpath(__file__))+"\\upload"

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/cargardatos', methods = ['GET', 'POST'])
def cargarDatos():
   if request.method == 'POST':
       pass

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files.getlist('ruta')
        for i in f:
            directory=i.filename
            if not os.path.exists(directory):
                os.makedirs(directory)
    i.save(os.path.join(app.config['UPLOAD_FOLDER'],(i.filename)))
    form=FormularioCargar.FormularioCargar()
    return render_template('cargar.html', form=form)
      
@app.route("/Cargar")
def cargar():
    form=FormularioCargar.FormularioCargar()
    return render_template('cargar.html', form=form)

@app.route("/Prediccion",methods = ['GET', 'POST'])
def prediccion():
    form=FormularioSeleccion.FormularioSeleccion()
    return render_template('prediccion.html', form=form)

@app.route("/Clustering")
def clustering():
    return render_template('clustering.html')

if __name__=="__main__":
    app.run(port=8000,debug=True)