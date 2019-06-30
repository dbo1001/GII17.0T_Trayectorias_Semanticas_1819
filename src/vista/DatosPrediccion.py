
class Singleton:
    __instance = None

    def __init__(self):
        if Singleton.__instance is not None:
            raise Exception("Cannot be instantiated twice!")
        Singleton.__instance = self
        self.proceso=None
        self.cargados = None
        self.clasificador=None
        self.fmeasure=None
        self.precision=None
        self.recall=None
        self.aciertos=None
        self.fallos=None
        self.X=None
        self.df=None

    @staticmethod
    def get_instancia():
        if Singleton.__instance is None:
            Singleton()
        return Singleton.__instance