import sqlite3

conexao = sqlite3.connect('TCC_PegarChaves.db')
cursor = conexao.cursor()

class ChaveDAO:

    def __init__(self):
        None

    def cadastrar_chave(self, local):
        cursor.execute('INSERT INTO Chave VALUES (?)', (local,))
        conexao.commit()

    def retirar_chave(self, local, data, horario_saida, horario_chegada, matricula_responsavel):
        cursor.execute('INSERT INTO Chave em Circulacao VALUES (?,?,?,?,?)', (local, data, horario_saida, horario_chegada, matricula_responsavel))
        conexao.commit()

    def devolver_chave(self, local, horario_chegada):
        cursor.execute('UPDATE TABLE Chave em Circulacao SET horario_chegada = ? WHERE local = ?', (horario_chegada, local))
        conexao.commit()

    def buscar_chave_circulacao(self, local):
        for tupla in cursor.execute('SELECT * FROM Chave em Circulacao WHERE local = ?',(local,)):
            if tupla[0] == local:
                self.objeto_chave(tupla)

    def buscar_chave_com_responsavel(self, matricula):
        for tupla in cursor.execute('SELECT * FROM Chave em Circulacao WHERE responsavel = ?', (matricula, )):
            if tupla[4] == matricula:
                self.objeto_chave(tupla)

    def objeto_chave(self, tupla):
        from chave import Chave
        return Chave(tupla[0], tupla[1], tupla[2], tupla[3], tupla[4])

    def chaves_em_circulacao(self):
        for tupla in cursor.execute('SELECT * FROM Chave em Circulacao WHERE horario_chegada = "-----" '):
            lista_chaves = []
            lista_chaves.append(self.objeto_chave(tupla))
        return lista_chaves

    def relacao_de_chaves_retiradas(self):
        for tupla in cursor.execute('SELECT * FROM Chave em Circulacao'):
            lista_chaves = []
            lista_chaves.append(self.objeto_chave(tupla))
        return lista_chaves

