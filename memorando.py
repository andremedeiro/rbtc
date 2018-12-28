
class Memorando:

    def __init__(self,local, professor, aluno,  inicio, encerramento, situacao):
        self.professor = professor
        self.aluno = aluno
        self.local = local
        self.inicio = inicio
        self.encerramento = encerramento
        self.situacao = situacao

    def __str__(self):
        return('{}: O(A) DOCENTE {} PERMINTIU  {} ACESSO A(AO) {} DE {} Á {}'.format(self.situacao,self.professor,self.aluno, self.local, self.inicio, self.encerramento))

    def get_professor(self):
        return self.professor

    def get_aluno(self):
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

    def set_aluno(self, novo):
        self.aluno = novo

    def set_inicio(self, novo):
        self.inicio = novo

    def set_encerramento(self, novo):
        self.encerramento = novo

    def set_situacao(self, novo):
        self.situacao = novo

    def set_local(self, local):
        self.local = local

