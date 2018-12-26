import time
from memorandoDAO import MemorandoDAO
memorandoDAO=MemorandoDAO()

class Memorando:

    def __init__(self,local, professor, lista_alunos,  inicio, encerramento, situacao):
        self.professor = professor
        self.lista_alunos = lista_alunos
        self.local = local
        self.inicio = inicio
        self.encerramento = encerramento
        self.situacao = situacao

    def __str__(self):
        return('\nO(A) DOCENTE {} PERMINTIU AOS ALUNOS {} ACESSO A CHAVE DO(DA) {} DE {} Á {}'.format(self.professor,self.lista_alunos, self.local, self.inicio, self.encerramento))

    def get_professor(self):
        return self.professor

    def get_alunos(self):
        return self.lista_alunos

    def get_inicio(self):
        return self.inicio

    def get_encerramento(self):
        return self.encerramento

    def get_situacao(self):
        return self.situacao

    def get_local(self):
        return self.local

    def set_professor(self, novo):
        self.professor = novo

    def set_lista_alunos(self, novo):
        self.lista_alunos = novo

    def set_inicio(self, novo):
        self.inicio = novo

    def set_encerramento(self, novo):
        self.encerramento = novo

    def set_situacao(self, novo):
        self.situacao = novo

    def set_local(self, local):
        self.local = local









































