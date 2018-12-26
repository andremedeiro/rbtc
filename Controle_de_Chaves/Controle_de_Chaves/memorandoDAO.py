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
        cursor = conexao.cursor()

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

    def insere_memorando(self,  local, professor, aluno, inicio, encerramento):
        cursor = conexao.cursor()
        situacao = self.analisa_situacao(encerramento)
        cursor.execute('insert into Memorando values (?,?,?,?,?,?)',(local, professor, aluno, inicio, encerramento, situacao))
        conexao.commit()
        cursor.close()

    def buscar_autorizacao(self, matricula, local):
        cursor = conexao.cursor()
        for memorando in cursor.execute('select * from Memorando where local = ? and situacao = "VALIDO"', (local,)):
            if memorando[2] == matricula:
                return True
        cursor.close()

    def listar_memorandos(self):
        cursor = conexao.cursor()
        memorandos = []
        for memorando in cursor.execute('select * from Memorando'):
            lista_alunos = []
            memorando_lista = list(memorando)
            lista_alunos.append(memorando_lista[2])
            memorando_lista.pop(2)
            memorando_lista.insert(2, lista_alunos)
            memorandos.append(memorando_lista)
        memorandos_feitos = []
        for memorando in memorandos:
            local = memorando[0]
            professor = memorando[1]
            lista_alunos = memorando[2]
            for outro_memorando in memorandos:
                if outro_memorando[0] == local and outro_memorando[1] == professor:
                    aluno = outro_memorando[2]
                    lista_alunos.append(aluno[0])
                    memorandos.remove(outro_memorando)
            memorandos_feitos.append(self.retorna_objeto(memorando))
        return(memorandos_feitos)

        cursor.close()

    def memorando_validos(self):
        cursor = conexao.cursor()
        memorandos = []
        for memorando in cursor.execute('select * from Memorando where situacao = "VALIDO"'):
            lista_alunos = []
            memorando_lista = list(memorando)
            lista_alunos.append(memorando_lista[2])
            memorando_lista.pop(2)
            memorando_lista.insert(2, lista_alunos)
            memorandos.append(memorando_lista)
        memorandos_feitos = []
        for memorando in memorandos:
            local = memorando[0]
            professor = memorando[1]
            lista_alunos = memorando[2]
            for outro_memorando in memorandos:
                if outro_memorando[0] == local and outro_memorando[1] == professor:
                    aluno = outro_memorando[2]
                    lista_alunos.append(aluno[0])
                    memorandos.remove(outro_memorando)
            memorandos_feitos.append(self.retorna_objeto(memorando))
        return (memorandos_feitos)
        cursor.close()

    def retorna_objeto(self, tupla):
        cursor = conexao.cursor()
        from memorando import Memorando
        memorando = Memorando(tupla[0],tupla[1],tupla[2],tupla[3],tupla[4],tupla[5])
        return memorando
        cursor.close()

