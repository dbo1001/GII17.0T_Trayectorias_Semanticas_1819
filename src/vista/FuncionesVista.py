from load.LoadCSV import LoadCSV 
from load.ConfiguracionDeLectura import ConfiguracionDeLectura as CDL
from load.CrearTrayectoriaB import CrearTrayectoriaB
from SQL import SQLInsert as si
from load.Contadores import idUsuario
from modelo.TrayectoriaConceptual import TrayectoriaConceptual

from SQL import SQLSelect as ss
from prediccion import Probador as pro
from prediccion import Conversor as con
from vista import DatosPrediccion
from prediccion import ClasificadorPrediccion as cp

def cargarDatosCSV2SQL(x,y,t,ts,exten,lineaIni,dir):
    try:
        contaUsu=idUsuario()
        r=list()
        cdl=CDL(x=x,y=y,t=t,ts=ts,extension=exten,lineaIni=lineaIni)
        usuarios=list()
        conceptuales=list()
        conta=0
        #lectorCSV=LoadCSV(x,y,[(5,"%Y-%m-%d"),(6,"%H:%M:%S")],exten,'epsg:4326',6)
        lectorCSV=LoadCSV(cdl)
        for i in lectorCSV.rutasPorUsuario(dir):
            usuario=contaUsu.cId()
            usuarios.append(usuario)
            procesar=CrearTrayectoriaB(args=[i,usuario,0,1,2,3])
            r.extend(procesar.run())
            for j in range(len(r)):
                conceptuales.append(TrayectoriaConceptual(r[j]))
            si.insertUsuarios(usuarios)
            si.insertTrayectoria(r)
            si.insertarTrayectoriaConceptual(conceptuales)
            print(conta)
            r=list()
            conceptuales=list()
            usuarios=list()
            conta+=1
            return True      
    except:
        return "Error: Los datos introducidos son incorrectos"
def provarClasificador(listasOSM):
    p=pro.Probador(listasOSM)
    for i in range(50):
        p.validacionCruzada("category",division=5,minSupport=0.01*i)

    return p.getEstadisticos()
    #p.graficos()
def predecir(listasOSM):
    pass


def cargarRutas(From,Where):
    datos=DatosPrediccion.Singleton.get_instancia()
    try:
        conversor=con.Conversor()
        ltc=ss.cargarTrayectoriasConceptuales(From=From, Where=Where)
        lts=conversor.TCtoTS(ltc)
        listasOSM=conversor.TStoIdOSM(lts)
        lx=listasOSM.copy()
        datos.cargados=lts
        
        if datos.clasificador is None:
            if len(listasOSM)<5:
                datos.cargados=-2
            else:
                p=pro.Probador(listasOSM)
                fmeasure,precision,recall,aciertos,fallos=p.validacionCruzada("category",division=5,minSupport=0.01)
                datos.fmeasure=round(fmeasure,2)
                datos.precision=round(precision,2)
                datos.recall=round(recall,2)
                datos.aciertos=aciertos
                datos.fallos=fallos
                X=conversor.combertirACategorias(listasOSM)
                datos.clasificador=cp.ClasificadorPrediccion().fit(X)
        else:
            datos.X=conversor.combertirACategorias(lx)

    except:
        datos.cargados=-1


##153
#conversor=con.Conversor()
#clus=CM.ClusteringMatrices()
#for i in [3]:
#    ltc=ss.cargarTrayectoriasConceptuales(From="from parado", Where="where  trayectoria.id_usuario="+str(i)+" ")
#    listasOSM=conversor.TStoIdOSM(conversor.TCtoTS(ltc))
#    p=pro.Probador(listasOSM)
#    for i in range(50):
#        p.validacionCruzada("category",division=5,minSupport=0.01*i)
#
#    print(p.getEstadisticos())
#    p.graficos()