import sqlite3

conexao = sqlite3.connect('TCC_PegarChaves.db')
cursor = conexao.cursor()

class ResponsavelDAO:
    def __init__(self):
        None

    def buscar_responsavel(self, matricula):
        for tupla in cursor.execute('SELECT * FROM Responsavel WHERE matricula = ? ', (matricula,)):
            return self.objeto_responsavel(tupla)

    def cadastrar_responsavel(self,nome, matricula):
        tipo = self.analisar_matricula(matricula)
        cursor.execute('INSERT INTO Responsavel VALUES (?,?,?)', (nome,matricula, tipo))
        conexao.commit()

    def objeto_responsavel(self, tupla):
        from responsavel import Responsavel
        return Responsavel(tupla[0], tupla[1], tupla[2])

    def analisar_matricula(self, matricula):
        if len(matricula) == 7:
            return 'DOCENTE'
        elif len(matricula) == 11 or len(matricula) == 12:
            return 'DISCENTE'

