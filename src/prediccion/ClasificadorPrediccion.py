# -*- coding: utf-8 -*-
"""
Created on Thu May  2 14:43:46 2019

@author: Hector
"""
from sklearn.base import BaseEstimator, ClassifierMixin
import pandas as pd
class nodo():
    def __init__(self,se=str(),su=1.0):
        self.__semantic=se
        self.__support=su
        self.__children=dict()
    def setSemantic(self,s:str()):
        self.__semantic=s
    def setSupport(self,s:float()):
        self.__support=s
    def addChild(self,k,v):
        self.__children[k]=v
    def getChildren(self,k):
        if k in self.__children:
            return self.__children[k]
        else:
            return None
    def existChildren(self,k):
        if k in self.__children:
            return True
        else:
            return False
    def getSupport(self):
        return self.__support
    def getChildrenList(self):
        return list(self.__children.values())
    def getSemantic(self):
        return self.__semantic
    def __str__(self):
        return self.__semantic
class ClasificadorPrediccion(BaseEstimator,ClassifierMixin):  
    """Un ejemplo de clasificador que utiliza un DecisionTree"""
    
    def __init__(self,frequent=7,a=0.8):
        """
        Constructor.
        
        Aunque no sea obligatorio, es recomendable que todos los parámetros 
        del constructor tengan valores por defecto.
        
        Como este clasificador solo copia a DecisionTree no tiene parámetros
        """
        self.root = nodo()
        self.__frequent=frequent
        self.__a=a
        self.__frecuencias=dict()


    def fit(self, X, y=None):
        """
        En un clasificador "real" todo el trabajo debe de hacerse aquí
        Consejo: Es una buena idea utilizar aserciones en lugar de try/except
        """
        import pandas as pd
        from prefixspan import PrefixSpan
        
        l=list()
        p=PrefixSpan(X)
        for i in range(2,self.__frequent+1):
            l.extend(p.frequent(i))
        df=pd.DataFrame(columns=["secuencia","support","tam"])
        for i,j in enumerate(l):
            df.loc[i]=[j[1],j[0]/len(X),len(j[1])]
        df=df.sort_values("tam",ascending=True)
        df.drop("tam",axis=1,inplace=True)
        #df=df[df["support"] >= 0.5]
        df=df.reset_index(drop=True)
        
        
        for i in df.iterrows():
            node=self.root
            for pos,j in enumerate(i[1]["secuencia"]):
                if node.existChildren(j):
                    node=node.getChildren(j)
                    if pos==len(i[1]["secuencia"])-1:
                        node.setSupport(i[1]["support"])
                else:
                    child=nodo(se=j,su=i[1]["support"])
                    node.addChild(j,child)
                    node=child

        return self

   

    def predict(self, X, y=None):
        
        def prediccion(arbol,trayectoria,a):
            candidate=pd.DataFrame(columns=["ruta","score"])
            for i in range(1,len(trayectoria)+1):
                node=arbol
                candidateSequence=list()
                candidateScore=0
                salir=False
                for j in range(i,len(trayectoria)+1):
                    if node.existChildren(trayectoria[j-1]):
                        node=node.getChildren(trayectoria[j-1])
                        candidateSequence.append(trayectoria[j-1])
                        candidateScore=candidateScore+(a**(len(trayectoria)-j)*node.getSupport())
                    else:
                        salir=True
                        break

                if not(salir):
                    root=arbol
                    for i in candidateSequence:
                        root=root.getChildren(i)
                    for i in root.getChildrenList():
                        candidate.loc[len(candidate)]=[i.getSemantic(),candidateScore+i.getSupport()]
            if len(candidate)>0:
                ret=3
                if len(candidate)<2:
                    ret=len(candidate)
                candidate=candidate.groupby(["ruta"],as_index=False).sum()
                return candidate.sort_values(by="score", ascending=False).iloc[0:ret]['ruta'].tolist()
            else:
                return None
        return prediccion(self.root,X,self.__a)
        

    def score(self, X, y=None):
        # devuelve el valor de la medida que maximiza o minimiza el clasificador
        pass
if __name__ == "__main__":
    import numpy as np
    clasificador=ClasificadorPrediccion()
    setB=list()
    setB.append(np.array(["s","b","p","r"]))
    setB.append(np.array(["u","s","b","p","h"]))
    setB.append(np.array(["u","s","p","h"]))
    tr=np.array(["u","s"])
    
    clasificador.fit(setB)
    l = clasificador.predict(tr)
    print(l)