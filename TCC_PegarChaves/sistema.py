from chaveDAO import ChaveDAO
from responsalvelDAO import ResponsavelDAO
from datetime import datetime
import sqlite3

conexao = sqlite3.connect('TCC_PegarChaves.db')
cursor = conexao.cursor()

chaveDAO = ChaveDAO()
ressponsavelDAO = ResponsavelDAO()

class Sistema:

    def __init__(self):
        None

#--------------    RESPONSAVEL    ----------------

    def cadastrar_responsavel(self, nome, matricula, tipo):
        ressponsavelDAO.cadastrar_responsavel(nome, matricula, tipo)

    def buscar_responsavel(self, matricula):
        ressponsavelDAO.buscar_responsavel(matricula)



#-----------------    CHAVE    -------------------

    def cadastrar_chave(self, local):
        chaveDAO.cadastrar_chave(local)

    def retirar_chave(self, local, matricula_responsavel):
        data = self.data_atual()
        horario_saida = self.hora_atual()
        chaveDAO.retirar_chave(local, data, horario_saida, "-----", matricula_responsavel)

    def devolver_chave(self, local):
        horario_chegada = self.hora_atual()
        chaveDAO.devolver_chave(local, horario_chegada)

    def imprimir_relacao_diaria(self):
        None

    def chaves_em_circulacao(self):
        chaveDAO.chaves_em_circulacao()

    def data_atual(self):
        now = datetime.now()
        dia = now.day
        mes = now.month
        ano = now.year
        return (str(dia) + "/" + str(mes) + "/" + str(ano))

    def hora_atual(self):
        now = datetime.now()
        hora = now.hour
        minuto = now.minute
        return (str(hora) + ':' + str(minuto))

#---------------    MEMORANDO    -----------------




