from responsalvelDAO import *

responsavelDAO = ResponsavelDAO()

class Responsavel:

    def __init__(self, nome, matricula, tipo):
        self.nome = nome
        self.matricula = matricula
        self.tipo = tipo

    def get_nome(self):
        return self.nome

    def get_matricula(self):
        return self.matricula

    def get_tipo(self):
        return self.tipo

    def set_nome(self, novo):
        self.nome = novo

    def set_matricula(self, novo):
        self.matricula = novo

    def set_tipo(self, novo):
        self.tipo = novo

