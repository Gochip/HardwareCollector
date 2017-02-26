class SistemaOperativo():
    def __init__(self, nombre = None, version = None):
        self.nombre = nombre
        self.version = version

    def set_nombre(self, nombre):
        self.nombre = nombre

    def set_nombre(self, version):
        self.version = version

    def get_nombre(self):
        return self.nombre

    def get_version(self):
        return self.version
