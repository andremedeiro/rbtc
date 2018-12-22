from usuarioDAO import UsuarioDAO
usuarioDAO=UsuarioDAO()

class Usuario:

    def __init__(self, nome, matricula, tipo):
        self.nome = nome
        self.matricula = matricula
        self.tipo = tipo

    def __str__(self):
        return ('\n{}: {} | MATRICULA: {}'.format(self.tipo, self.nome, self.matricula))

    def get_nome(self):
        return self.nome

    def get_matricula(self):
        return self.matricula

    def get_tipo(self):
        return self.tipo

    def set_tipo(self, novo):
        self.tipo = novo

    def set_matricula(self, novo):
        self.matricula = novo

    def set_nome(self, novo):
        self.nome=novo











