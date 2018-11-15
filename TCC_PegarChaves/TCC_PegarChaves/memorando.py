import time

class Memorando:

    def __init__(self, professor, lista_de_alunos, inicio, encerramento, situacao):
        self.professor = professor
        self.alunos = lista_de_alunos
        self.inicio = self.ajeita_data(inicio)
        self.encerramento = self.ajeita_data(encerramento)
        self.situacao = situacao

    def get_professor(self):
        return self.professor

    def get_alunos(self):
        return self.alunos

    def get_inicio(self):
        return self.inicio

    def get_encerramento(self):
        return self.encerramento

    def get_situacao(self):
        return self.situacao

    def set_professor(self, novo):
        self.professor = novo

    def set_lista_alunos(self, novo):
        self.alunos = novo

    def set_inicio(self, novo):
        self.inicio = novo

    def set_encerramento(self, novo):
        self.encerramento = novo

    def set_situacao(self, novo):
        self.situacao = novo

    def ajeita_data(self, data):
        return time.strptime(data, "%d/%m/%Y")
