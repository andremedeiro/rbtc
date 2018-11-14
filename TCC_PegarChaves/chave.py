from chaveDAO import ChaveDAO
from datetime import datetime
import time

class Chave:

    def __init__(self, local):
        self.local = local
        self.data = None
        self.horario_saida = None
        self.horario_entrega = None
        self.responsavel = None

# Os métodos com inicio "get" e "set" têm como objetivo dar uma maior segurança aos dados, evitando que haja um acesso externo diretamente nos atributos do objeto

    def get_local(self):
        return self.local

    def get_data(self):
        return self.data

    def get_responsalvel(self):
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

# O método data_atual pega data atual do computador

    def data_atual(self):
        now = datetime.now()
        dia = now.day
        mes = now.month
        ano = now.year
        return (str(dia) + "/" + str(mes) + "/" + str(ano))