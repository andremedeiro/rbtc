import sqlite3
import time
from datetime import datetime
conexao = sqlite3.connect("Controle_de_Chave.db")

class MemorandoDAO:

    def __init__(self):
        self.criar_tabela()
        self.ajeitar_situacoes()

    def criar_tabela(self):
        cursor = conexao.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS Memorando (local text, professor text, aluno text, inicio text, encerramento text, situacao text, foreign key(local) references Chave(local), foreign key(professor) references Usuario(matricula), foreign key (aluno) references Usuario(matricula))')
        cursor.close()

    def ajeitar_situacoes(self):
        if len(self.listar_memorandos()) != 0:
            cursor = conexao.cursor()
            for memorando in cursor.execute('select * from Memorando'):
                if memorando != None:
                    situacao=self.analisa_situacao(memorando[4])
                    cursor.execute('update Memorando set situacao = ? where local = ? and professor = ? and aluno = ?',(situacao, memorando[0], memorando[1], memorando[2]))
            cursor.close()

    def data_atual(self):
        now = datetime.now()
        dia = now.day
        mes = now.month
        ano = now.year
        return (str(dia) + "/" + str(mes) + "/" + str(ano))

    def analisa_situacao(self, data):
        data_de_hoje = time.strptime(self.data_atual(), "%d/%m/%Y")
        data = time.strptime(data, "%d/%m/%Y")
        if data < data_de_hoje:
            return 'INVALIDO'
        else:
            return 'VALIDO'

    def insere_memorando(self,  local, professor, aluno, encerramento):
        cursor = conexao.cursor()
        situacao = self.analisa_situacao(encerramento)
        data_atual=self.data_atual()
        cursor.execute('insert into Memorando values (?,?,?,?,?,?)',(local, professor, aluno, data_atual, encerramento, situacao))
        conexao.commit()
        cursor.close()

    def buscar_autorizacao(self, matricula, local):
        cursor = conexao.cursor()
        for memorando in cursor.execute('select * from Memorando where local = ? and situacao = "VALIDO"', (local,)):
            if memorando[2] == matricula:
                return True
        cursor.close()

    def remove(self,matricula):
        cursor=conexao.cursor()
        try:
            int(matricula)
        except:
            cursor.execute('delete from Memorando where local = ?',(matricula,))
        else:
            if len(matricula)==7:
                cursor.execute('delete from Memorando where professor = ?', (matricula,))
            else:
                cursor.execute('delete from Memorando where aluno = ?', (matricula,))
        conexao.commit()
        cursor.close()

    def listar_memorandos(self):
        cursor = conexao.cursor()
        memorandos = []
        for memorando in cursor.execute('select * from Memorando'):
            memorandos.append(self.retorna_objeto(memorando))
        return (memorandos)
        cursor.close()

    def retorna_objeto(self, tupla):
        from memorando import Memorando
        memorando = Memorando(tupla[0],tupla[1],tupla[2],tupla[3],tupla[4],tupla[5])
        return memorando
