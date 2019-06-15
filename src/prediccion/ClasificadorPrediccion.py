# -*- coding: utf-8 -*-
"""
Created on Thu May  2 14:43:46 2019

@author: Hector
"""
from sklearn.base import BaseEstimator, ClassifierMixin
import pandas as pd
class nodo():
    '''
    Esta clase esta diseñada para ser los nodos del árbol de clasificación “ClasificadorPrediccion”.

    Args:
        se (str): Semántica del nodo.
        su (float): Soporte del nodo.
        
    Attributes:
        __semantic (str): Almacena la semántica del nodo.
        __support (float): Almacena el soporte del nodo.
        __children (dict): Almacena los nodos hijo de este nodo.
        
    '''
    def __init__(self,se=str(),su=1.0):
        self.__semantic=se
        self.__support=su
        self.__children=dict()
    def setSemantic(self,s:str()):
        '''
        Función de tipo SET que modifica la semántica de un nodo.

        Args:
            s (str): Nuevo valor para la semántica.
            
        Raises:

        Returns:
            
        '''
        self.__semantic=s
    def setSupport(self,s:float()):
        '''
        Función de tipo SET que modifica el soporte de un nodo.

        Args:
            s (float): Nuevo valor para el soporte.
            
        Raises:

        Returns:
            
        '''
        self.__support=s
    def addChild(self,k,v):
        '''
        Función que añade un nuevo hijo al nodo.

        Args:
            k (str): Clave del nodo “semantic”.
            v (nodo): El nodo que se va a añadir a los hijos del nodo actual.
            
        Raises:

        Returns:
            
        '''
        self.__children[k]=v
    def getChildren(self,k):
        '''
        Función de tipo GET que devuelve el hijo del nodo actual al que corresponde la clave recibida.

        Args:
            k (str): Clave del hijo del nodo actual.
            
        Raises:

        Returns:
            node: Retorna el hijo si existe y None si no existe.
            
        '''
        if k in self.__children:
            return self.__children[k]
        else:
            return None
    def existChildren(self,k):
        '''
        Función que devuelve si existe en este nodo un nodo hijo con la clave recibida.

        Args:
            k (str): Clave del nodo que estamos buscando.
            
        Raises:

        Returns:
            boolean: True si existe, False si no existe.
            
        '''
        if k in self.__children:
            return True
        else:
            return False
    def getSupport(self):
        '''
        Función de tipo GET que devuelve el soporte del nodo.
        
        Args:
            
        Raises:

        Returns:
            float: Retorna el soporte del nodo.
            
        '''
        return self.__support
    def getChildrenList(self):
        '''
        Función de tipo GET que devuelve la lista de hijos del nodo.
        
        Args:
            
        Raises:

        Returns:
            list: Lista con todos los nodos hijos de este nodo.
            
        '''
        return list(self.__children.values())
    def getSemantic(self):
        '''
        Función de tipo GET que devuelve el valor de la semántica del nodo.
        
        Args:
            
        Raises:

        Returns:
            str: Retorna el valor de la semántica de este nodo.
            
        '''
        return self.__semantic
    def __str__(self):
        return self.__semantic
class ClasificadorPrediccion(BaseEstimator,ClassifierMixin):  
    
    def __init__(self,frequent=7,a=0.8,minSupport=0.05):
        """
        Constructor.
        
        Aunque no sea obligatorio, es recomendable que todos los parámetros 
        del constructor tengan valores por defecto.

        """
        self.root = nodo()
        self.__frequent=frequent
        self.__a=a
        self.__frecuencias=dict()
        self.__minSupport=minSupport


    def fit(self, X, y=None):

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
        df=df[df["support"] >= self.__minSupport]
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
                ret=1
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