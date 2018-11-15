from chaveDAO import ChaveDAO
import time

class Chave:

    def __init__(self, local, data = None, horario_saida = None, horario_entrega = None, responsavel = None):
        self.local = local
        self.data = data
        self.horario_saida = horario_saida
        self.horario_entrega = horario_entrega
        self.responsavel = responsavel

    def __str__(self):
        if self.responsavel == None:
            return "| "+self.local +" |"
        elif self.responsavel != None and self.horario_entrega == None:
            return ("| " + self.local + " | " + self.responsavel + ' | ' + self.data + ' | ' + self.horario_saida)
        else:
            return ("| " + self.local + " | " + self.responsavel + ' | ' + self.data + ' | Retirada: ' + self.horario_saida + ' | Desvolvida: ' + self.horario_entrega)

    def get_local(self):
        return self.local

    def get_data(self):
        return self.data

    def get_responsavel(self):
        return self.responsavel

    def get_horario_saida(self):
        return self.horario_saida

    def get_horario_entrega(self):
        return self.horario_entrega

    def set_local(self, novo):
        self.local = novo

    def set_data(self, novo):
        self.data = novo

    def set_responsavel(self, novo):
        self.responsavel = novo

    def set_horario_saida(self, novo):
        self.horario_saida = novo

    def set_horario_entrega(self, novo):
        self.horario_entrega = novo

