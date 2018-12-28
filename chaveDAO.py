import sqlite3
from datetime import datetime
conexao = sqlite3.connect("Controle_de_Chave.db")

class ChaveDAO:

    def __init__(self):
        self.criar_tabelas()

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

    def criar_tabelas(self):
        cursor = conexao.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS Chave (local TEXT PRIMARY KEY)')
        cursor.execute('CREATE TABLE IF NOT EXISTS Chave_em_Circulacao (local TEXT, usuario_retirada TEXT, data_retirada TEXT, horario_saida TEXT, data_entrega TEXT,horario_entrega TEXT, usuario_entrega TEXT, FOREIGN KEY(local) REFERENCES Chave ( local ), FOREIGN KEY(usuario_retirada) REFERENCES Usuario( matricula ),FOREIGN KEY(usuario_entrega) REFERENCES Usuario ( matricula ))')
        cursor.close()

    def insere_chave(self, local):
        cursor = conexao.cursor()
        cursor.execute('INSERT INTO Chave VALUES (?)', (local,))
        conexao.commit()
        cursor.close()

    def retira_chave(self, local,  matricula_usuario):
        cursor = conexao.cursor()
        cursor.execute('insert into Chave_em_Circulacao values(?,?,?,?,?,?,?)',(local,matricula_usuario,self.data_atual(), self.hora_atual(),'-','-','-'))
        conexao.commit()
        cursor.close()

    def devolve_chave(self, local, matricula_usuario):
        cursor = conexao.cursor()
        for transicao in cursor.execute('select * from Chave_em_Circulacao where usuario_entrega = "-"'):
            if transicao[0] == local:
                cursor.execute('update Chave_em_Circulacao set data_entrega = ? where local = ? and data_entrega = "-"', (self.data_atual(), local))
                cursor.execute('update Chave_em_Circulacao set horario_entrega = ? where local = ? and horario_entrega = "-"', (self.hora_atual(), local))
                cursor.execute('update Chave_em_Circulacao set usuario_entrega = ? where local = ? and usuario_entrega = "-"', (matricula_usuario, local))
                conexao.commit()
        cursor.close()

    def listar_chaves(self):
        cursor = conexao.cursor()
        lista_chaves=[]
        for tupla in cursor.execute('select * from Chave'):
            if tupla != None:
                lista_chaves.append(self.objeto_chave(tupla))
        cursor.close()
        return lista_chaves


    def buscar_chave(self, local):
        cursor = conexao.cursor()
        for chave in cursor.execute('select * from Chave'):
            if chave != None:
                if chave[0] == local:
                    return self.objeto_chave(chave)
        cursor.close()

    def chaves_em_circulacao(self):
        cursor = conexao.cursor()
        lista_transacoes = []
        for chave in cursor.execute('select * from Chave_em_Circulacao where usuario_entrega = "-"'):
            if chave != None:
                lista_transacoes.append(self.objeto_chave_circulacao(chave))
        cursor.close()
        return lista_transacoes

    def remover_chave(self, local):
        cursor = conexao.cursor()
        cursor.execute('delete from Chave where local = ?',(local,))
        conexao.commit()
        cursor.close()

    def objeto_chave(self, tupla):
        from chave import Chave
        chave=Chave(tupla[0])
        return chave

    def objeto_chave_circulacao(self, tupla):
        from chave import Chave
        chave = Chave(tupla[0], tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6])
        return chave