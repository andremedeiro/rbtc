import sqlite3
import time
from datetime import datetime
conexao = sqlite3.connect('TCC_PegarChaves.db')
cursor = conexao.cursor()

class MemorandoDAO:

    def __init__(self):
        None

    def buscar_permissao(self, matricula):
        for tupla in cursor.execute('SELECT * FROM Memorando'):
            if matricula == tupla[1]:
                return True

    def cadastrar_memorando(self, professor, aluno, inicio, encerramento):
        situacao = self.analisa_situacao(encerramento)
        cursor.execute('INSERT INTO Memorando VALUES (?,?,?,?,?)', (professor, aluno, inicio, encerramento, situacao))
        conexao.commit()

    def analisa_situacao(self, data):
        data_de_hoje = time.strptime(self.data(), "%d/%m/%Y")
        data = time.strptime(data, "%d/%m/%Y")
        if data < data_de_hoje:
            return False
        else:
            return True

    def data(self):
        now = datetime.now()
        dia = now.day
        mes = now.month
        ano = now.year
        return (str(dia) + "/" + str(mes) + "/" + str(ano))

    def objeto_memorando(self, tupla):
        from memorando import Memorando
        return Memorando(tupla[0], tupla[1], tupla[2], tupla[3], tupla[4])

