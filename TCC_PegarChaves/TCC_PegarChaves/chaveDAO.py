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
        cursor.execute('INSERT INTO Chave_em_Circulacao VALUES (?,?,?,?,?)', (local, data, horario_saida, horario_chegada, matricula_responsavel))
        conexao.commit()

    def devolver_chave(self, local, horario_entrega):
        cursor.execute('UPDATE Chave_em_Circulacao SET horario_entrega = ? WHERE local = ?', (horario_entrega, local))
        conexao.commit()

    def buscar_chave(self, local):
        for tupla in cursor.execute('SELECT * FROM Chave WHERE local = ?', (local,)):
            if tupla[0] == local:
                return self.objeto_chave(tupla)

    def buscar_chave_circulacao(self, local):
        for tupla in cursor.execute('SELECT * FROM Chave_em_Circulacao WHERE local = ? and horario_entrega = "-----"',(local,)):
            if tupla[0] == local:
                return self.objeto_chave_circulacao(tupla)

    def buscar_chave_com_responsavel(self, matricula):
        for tupla in cursor.execute('SELECT * FROM Chave_em_Circulacao WHERE responsavel = ?', (matricula, )):
            if tupla[4] == matricula:
                return self.objeto_chave_circulacao(tupla)

    def objeto_chave_circulacao(self, tupla):
        from chave import Chave
        return Chave(tupla[0], tupla[1], tupla[2], tupla[3], tupla[4])

    def objeto_chave(self, tupla):
        from chave import Chave
        return Chave(tupla[0])

    def chaves_em_circulacao(self):
        lista_chaves = []
        for tupla in cursor.execute('SELECT * FROM Chave_em_Circulacao WHERE horario_entrega = "-----" '):
            lista_chaves.append(self.objeto_chave_circulacao(tupla))
        return lista_chaves

    def relacao_de_chaves_retiradas(self):
        lista_chaves = []
        for tupla in cursor.execute('SELECT * FROM Chave em Circulacao'):
            lista_chaves.append(self.objeto_chave_circulacao(tupla))
        return lista_chaves

    def chaves_em_geral(self):
        lista_chaves = []
        for tupla in cursor.execute('SELECT * FROM Chave'):
            lista_chaves.append(self.objeto_chave(tupla))
        return lista_chaves

