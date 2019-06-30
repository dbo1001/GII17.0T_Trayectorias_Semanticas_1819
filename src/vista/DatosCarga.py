class Singleton:
    __instance = None

    def __init__(self):
        if Singleton.__instance is not None:
            raise Exception("Cannot be instantiated twice!")
        Singleton.__instance = self
        self.proceso = None
        self.usuariosInicio=None

    @staticmethod
    def get_instancia():
        if Singleton.__instance is None:
            Singleton()
        return Singleton.__instance