# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 23:00:36 2019

@author: Hector
"""
from sklearn.cluster import DBSCAN
from sklearn.mixture import GaussianMixture
from SQL import SQLSelect as ss
from prediccion import Conversor as con

class ClusteringMatrices():
    def __init__(self):
        self.cluster=DBSCAN(n_jobs=-1)
        self.cluster2=GaussianMixture()
        pass
    def fit(self, X, y=None):
        
        self.cluster.fit(X)
        pass
    def predict(self, X, y=None):
        return self.cluster.fit_predict(X)
    def verInformacion(self):
        labels = self.cluster.labels_
        # Number of clusters in labels, ignoring noise if present.
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise_ = list(labels).count(-1)
        
        
        return n_clusters_,n_noise_

    def Clustering(self,ID_Usuario_ini=-1,ID_Usuario_fin=-1,agrupar=4):
        conversor=con.Conversor()
        maxi=0
        mini=0
        where=""
        mx=list()
        if ID_Usuario_ini!=-1:
            mini=ID_Usuario_ini
        else:
            mini=ss.selectApp('SELECT min(id_usuario) from usuario').iat[0,0]
        if ID_Usuario_fin!=-1:
            maxi=ID_Usuario_fin
        else:
            maxi=ss.selectApp('SELECT max(id_usuario) from usuario').iat[0,0]
        if agrupar==1:
            where=" and EXTRACT(ISODOW FROM date) IN (6, 7)"+where
            for i in range(mini,maxi):
                where="where  trayectoria.id_usuario="+str(i)+where
                ltc=ss.cargarTrayectoriasConceptuales(From="from parado", Where=where)
                listasOSM=conversor.TStoIdOSM(conversor.TCtoTS(ltc))
                mx.append(conversor.IdOSMtoMatrizClase(listasOSM))
        elif agrupar==2:
            where=" and EXTRACT(ISODOW FROM public.parado.instante_inicio) IN (1, 2, 3, 4, 5)"+where
            for i in range(mini,maxi):
                where="where  trayectoria.id_usuario="+str(i)+where
                ltc=ss.cargarTrayectoriasConceptuales(From="from parado", Where=where)
                listasOSM=conversor.TStoIdOSM(conversor.TCtoTS(ltc))
                mx.append(conversor.IdOSMtoMatrizClase(listasOSM))
        elif agrupar==3:
            where=" and EXTRACT(ISODOW FROM public.parado.instante_inicio) IN (1, 2, 3, 4, 5)"
            for i in range(mini,maxi):
                ltc=ss.cargarTrayectoriasConceptuales(From="from parado", Where="where  trayectoria.id_usuario="+str(i)+where)
                listasOSM=conversor.TStoIdOSM(conversor.TCtoTS(ltc))
                mx.append(conversor.IdOSMtoMatrizClase(listasOSM))
            where=" and EXTRACT(ISODOW FROM public.parado.instante_inicio) IN (6, 7)"
            for i in range(mini,maxi):
                ltc=ss.cargarTrayectoriasConceptuales(From="from parado", Where="where  trayectoria.id_usuario="+str(i)+where)
                listasOSM=conversor.TStoIdOSM(conversor.TCtoTS(ltc))
                mx.append(conversor.IdOSMtoMatrizClase(listasOSM))
        elif agrupar==4:
            for i in range(mini,maxi):
                where="where  trayectoria.id_usuario="+str(i)+where
                ltc=ss.cargarTrayectoriasConceptuales(From="from parado", Where=where)
                listasOSM=conversor.TStoIdOSM(conversor.TCtoTS(ltc))
                mx.append(conversor.IdOSMtoMatrizClase(listasOSM))
        r=self.predict(mx)
        r2=self.cluster2.fit_predict(mx)
        n_clusters,n_ruido=self.verInformacion()
        return n_clusters,n_ruido,r,r2