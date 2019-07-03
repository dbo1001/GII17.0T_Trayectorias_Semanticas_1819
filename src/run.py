# -*- coding: utf-8 -*-
"""
Created on Wed May 22 00:18:19 2019

@author: Hector
"""
import os
from flask import Flask
from flask import render_template,request,copy_current_request_context,redirect, url_for,send_file
from werkzeug import secure_filename
from formularios import FormularioCargar,FormularioSeleccion,FormularioExportar
from vista import FuncionesVista, DatosCarga, DatosPrediccion
from multiprocessing import Process
import threading
import shutil
import time

import pandas as pd
import geopandas as gpd

from SQL import SQLSelect as ss

app=Flask(__name__)
app.config['UPLOAD_FOLDER']=os.path.dirname(os.path.realpath(__file__))+"/upload"


@app.route("/")
def index():
    return render_template('index.html')

@app.route('/cargardatos', methods = ['GET', 'POST'])
def cargarDatos():
   if request.method == 'POST':
       pass


@app.route("/Cargar",methods = ['GET', 'POST'])
def cargar():
    form=FormularioCargar.FormularioCargar(request.form)
    print(form.validate())
    if request.method == 'POST':
        
        datosCargar=DatosCarga.Singleton.get_instancia()
        if datosCargar.proceso!=None and not(datosCargar.proceso.is_alive()):
            datosCargar.proceso=None
        datosCargar.usuariosInicio=ss.selectApp('SELECT max(id_usuario) from usuario').iat[0,0]
        mask=0o22
        shutil.rmtree(app.config['UPLOAD_FOLDER'], ignore_errors=False, onerror=None)
        f = request.files.getlist('ruta')
        mask=os.umask(mask)
        for i in f:
            directory=i.filename
            directory=directory.split("/")
            s=""
            for j in range(len(directory)-1):
                s=s+'/'+directory[j]
            if not os.path.exists(s):
                os.makedirs(app.config['UPLOAD_FOLDER']+s,mode=0o777,exist_ok=True)
            try:
                i.save(os.path.join(app.config['UPLOAD_FOLDER'],(i.filename)))
            except:
                return redirect(url_for("espera"), code=302)
        os.umask(mask)
        t=list()
        ts=list()
        t.append(int(request.form.get('columnaTiempo1')))
        ts.append((request.form.get('formatoTiempo1')))
        if request.form.get('columnaTiempo2')!="":
            t.append(int(request.form.get('columnaTiempo2')))
            ts.append((request.form.get('formatoTiempo2')))
        
        
        @copy_current_request_context
        def cargar_hilo(lon,lat,t,ts,exten,lIni,direc):
            FuncionesVista.cargarDatosCSV2SQL(lon,lat,t,ts,exten,lIni,direc)
        datosCargar.proceso=Process(target=cargar_hilo,args=(int(request.form.get('longitud')),int(request.form.get('latitud')),t,ts,request.form.get('extension'),int(request.form.get('lineainicio')),os.path.dirname(os.path.realpath(__file__))+"/upload"))
        datosCargar.proceso.start()
        return redirect(url_for("espera"), code=302)
        
    return render_template('cargar.html', form=form)

@app.route('/Cargar/espera',methods = ['GET'])
def espera():
    datosCargar=DatosCarga.Singleton.get_instancia()
    msg=""
    t="5"
    if datosCargar.proceso==None:
        msg="<h4> Error <h4>"
    elif datosCargar.proceso.is_alive():
        msg="<h2> Cargando... </h2> <div class=\"row justify-content-center\"><div class=\"spinner-border \" role=\"status\"><span class=\"sr-only\">Cargando...</span></div></div>"
    else:
        usuarioAhora=ss.selectApp('SELECT max(id_usuario) from usuario').iat[0,0]
        df=ss.selectApp("select trayectoria.id_usuario as ID_Usuario, (max(parado.id_trayectoria)-min(parado.id_trayectoria)+1) as Numero_Trayectorias,(max(parado.id_parada)-min(parado.id_parada)+1) as Numero_Paradas, (max(punto.id_punto)-min(punto.id_punto)+1) as Numero_Puntos from trayectoria, parado, punto where trayectoria.id_trayectoria=parado.id_trayectoria and trayectoria.id_trayectoria=punto.id_trayectoria and trayectoria.id_usuario>"+ str(datosCargar.usuariosInicio) +" group by trayectoria.id_usuario order by trayectoria.id_usuario")       
        msg="<h1> Resultado </h1> <button id=\"exportar\" type=\"button\" class=\"btn btn-dark\" onclick=\"exportTableToCSV('datos_carga.csv');\">Exportar</button> <br>"+df.to_html(index=False,classes="table table-striped table-dark")
        t="86400"
    return render_template('espera.html',msg=msg,t=t)

@app.route("/Prediccion",methods = ['GET', 'POST'])
def prediccion():
    msg=""
    msg2=""
    msg3=""
    msgA=""
    msgF=""
    msgFM=""
    msgP=""
    msgR=""
    msgNum=""
    btPre="disabled"
    btRe="disabled"
    datosCargar=DatosPrediccion.Singleton.get_instancia()

    @copy_current_request_context
    def cargar_hilo(From,Where):
        FuncionesVista.cargarRutas(From,Where)
    if not(datosCargar.df is None):
        msg3="<h1> Resultado </h1> <button id=\"exportar\" type=\"button\" class=\"btn btn-dark\" onclick=\"exportTableToCSV('datos_prediccion.csv');\">Exportar</button> <br>"+datosCargar.df.to_html(index=False,classes="table table-striped table-dark")
    if datosCargar.aciertos!=None:
        msgNum=datosCargar.aciertos+datosCargar.fallos
        msgA=datosCargar.aciertos
        msgF=datosCargar.fallos
        msgFM=datosCargar.fmeasure
        msgP=datosCargar.precision
        msgR=datosCargar.recall
    if datosCargar.cargados!=None and datosCargar.cargados!=-1 and datosCargar.cargados!=-2:
        msg2="<div class=\"alert alert-primary\" role=\"alert\">El clasificador esta entrenado</div>"
        if datosCargar.clasificador!=None and datosCargar.X!=None:
            btPre="enable"
            msg2="<div class=\"alert alert-primary\" role=\"alert\">El clasificador esta entrenado y hay datos para predecir</div>"

    form=FormularioSeleccion.FormularioSeleccion(request.form)
    if datosCargar.cargados==-2:
        msg="<div class=\"alert alert-danger\" role=\"alert\">No hay suficientes datos para entrenar</div>"
        datosCargar.proceso=None
        datosCargar.cargados=None
    if request.method=="POST":
        sqlFrom=" FROM public.parado "
        sqlWhere=""
        user=request.form.get("usuario")
        lunes=form.data["lunes"]
        martes=form.data["martes"]
        miercoles=form.data["miercoles"]
        jueves=form.data["jueves"]
        viernes=form.data["viernes"]
        sabado=form.data["sabado"]
        domingo=form.data["domingo"]
        taFrom=request.form.get("taFrom")
        taWhere=request.form.get("taWhere")
        lw=taWhere.lower().split(" ")
        dia=""

        sqlFrom=sqlFrom+" "+taFrom
        sqlWhere=sqlWhere+" "+taWhere
        if user!="":
            user=" and trayectoria.id_usuario="+str(user)
        else:
            user=""

        if not(lunes!=True and martes!=True and miercoles!=True and jueves!=True and viernes!=True and sabado!=True and domingo!=True):
            dia=" EXTRACT(ISODOW FROM parado.instante_inicio) IN (0 "
            if lunes:
                dia=dia+", 1"
            if martes:
                dia=dia+", 2"
            if miercoles:
                dia=dia+", 3"
            if jueves:
                dia=dia+", 4"
            if viernes:
                dia=dia+", 5"
            if sabado:
                dia=dia+", 6"
            if domingo:
                dia=dia+", 7"
            dia=dia+") "
        else:
            dia=" EXTRACT(ISODOW FROM parado.instante_inicio) IN (1,2,3,4,5,6,7) "
        if "where" in lw:
            sqlWhere=sqlWhere+" and "+dia+user
        else:
            sqlWhere=sqlWhere+" where  "+dia+user

        print(str(form.data))
        datosCargar.proceso=threading.Thread(target=cargar_hilo,args=(sqlFrom,sqlWhere))
        datosCargar.proceso.start()
        time.sleep(1)
        if datosCargar.cargados==-1:
            msg="<div class=\"alert alert-danger\" role=\"alert\">La consulta es incorrecta</div>"
            datosCargar.proceso=None
            datosCargar.cargados=None
        else:
            print(datosCargar.proceso,"render 1")
            return redirect(url_for("cargando"), code=302)
    return render_template('prediccion.html', form=form, msg=msg, btEn=btRe, btPre=btPre, msg2=msg2, msgA=msgA, msgF=msgF, msgFM=msgFM, msgP=msgP, msgR=msgR, msgNum=msgNum, msg3=msg3)

@app.route("/Exportar",methods = ['GET', 'POST'])
def exportar():
    form=FormularioExportar.FormularioExportar(request.form)
    msg=""
    if request.method=="POST":
        select=request.form.get("select")
        l=select.split(" ")
        ignore=False
        geo=False
        asterisco=False
        from_ = False
        for i in l:
            if not(ignore) or not(asterisco):
                if i.lower()=="from":
                    break
                elif i.lower() == "as":
                    ignore=True
                elif i.lower() == "punto" or i.lower() == "punto,":
                    geo=True
                    break
                elif i=="*":
                    asterisco=True
        for i in l:       
            if asterisco:
                if from_:
                    if i.lower()=="parado" or i.lower()=="parado," or i.lower()=="parado;" or i.lower()=="punto" or i.lower()=="punto," or i.lower()=="punto;":
                        geo=True
                elif i.lower()=="from":
                    from_=True
            else:
                break

            ignore=False
        if geo:
            df=ss.selectGDF(select)
        else:
            df=ss.selectApp(select)
        if not(isinstance(df,(pd.DataFrame, gpd.GeoDataFrame) )):
            msg="<div class=\"alert alert-danger\" role=\"alert\">La consulta no es valida</div>"
            return render_template('exportar.html',form=form,msg=msg)
        df.to_csv(os.path.dirname(os.path.realpath(__file__))+'/download/datos_exportados.csv', index = None, header=True)
        return send_file(os.path.dirname(os.path.realpath(__file__))+'/download/datos_exportados.csv', as_attachment=True)
    return render_template('exportar.html',form=form,msg=msg)

@app.route('/Prediccion/cargando',methods = ['GET'])
def cargando():
    datosCargar=DatosPrediccion.Singleton.get_instancia()
    msg=""
    if datosCargar.proceso==None:
        msg="<h4> Error <h4>"
    elif datosCargar.proceso.is_alive() :
        msg="<h2> Se están cargando los datos en el sistema, puede tardar unos minutos por favor espere </h2>"
    else:
        print(datosCargar.proceso,datosCargar.cargados)
        return redirect(url_for("prediccion"), code=302)
    return render_template('cargando.html',msg=msg)

@app.route('/Prediccion/reiniciar',methods = ['GET'])
def reiniciar():
    datosCargar=DatosPrediccion.Singleton.get_instancia()
    datosCargar.proceso=None
    datosCargar.cargados = None
    datosCargar.clasificador=None
    datosCargar.fmeasure=None
    datosCargar.precision=None
    datosCargar.recall=None
    datosCargar.aciertos=None
    datosCargar.fallos=None
    datosCargar.X=None
    datosCargar.df=None
    return redirect(url_for("prediccion"), code=302)
@app.route('/Prediccion/clasificar',methods = ['GET'])
def clasificar():
    df=pd.DataFrame(columns=["Id Usuario","Id Trayectoria","Trayectoria Categoria (3 ultimos)","Prediccion"])
    datosCargar=DatosPrediccion.Singleton.get_instancia()
    c=0
    for i in datosCargar.cargados:
        if len(i.getListOSMId())>2:
            pre=datosCargar.clasificador.predict(datosCargar.X[c])
            if not(pre is None):
                pre=pre[0]
            df.loc[len(df)]=[i.getUsuarioId(),i.getTrayectoriaId(),datosCargar.X[c][len(datosCargar.X[c])-3]+" "+datosCargar.X[c][len(datosCargar.X[c])-2]+" "+datosCargar.X[c][len(datosCargar.X[c])-1],pre]
            c+=1
    datosCargar.df=df
    return redirect(url_for("prediccion"), code=302)




if __name__=="__main__":
    app.run(host='0.0.0.0',port=8001,debug=False)
