from chaveDAO import ChaveDAO
from responsalvelDAO import ResponsavelDAO
from memorandoDAO import MemorandoDAO
from datetime import datetime
import sqlite3

conexao = sqlite3.connect('TCC_PegarChaves.db')
cursor = conexao.cursor()

chaveDAO = ChaveDAO()
responsavelDAO = ResponsavelDAO()
memorandoDAO = MemorandoDAO()

def mudar_cor(texto, cor):
    return str('\033[' + str(cor) + 'm' + str(texto) + '\033[0;0m')

class Sistema:

    def __init__(self):
        self.matricula_universal = '123'

#--------------    RESPONSAVEL    ----------------

    def cadastrar_responsavel(self, nome, matricula):
        responsavelDAO.cadastrar_responsavel(nome, matricula)

    def buscar_responsavel(self, matricula):
        if matricula == self.matricula_universal:
            return 'manutenção'
        else:
            return responsavelDAO.buscar_responsavel(matricula)

    def analizar_tipo(self, responsavel):
        if responsavel.get_tipo() == "Docente":
            return True
        elif responsavel.get_tipo() == "Discente":
            return False

#-----------------    CHAVE    -------------------

    def cadastrar_chave(self, local):
        chaveDAO.cadastrar_chave(local)

    def retirar_chave(self, local, matricula_responsavel):
        if self.chave_livre(local) == True:
            responsavel = self.buscar_responsavel(matricula_responsavel)
            print(mudar_cor(('\nO ' + responsavel.get_tipo() + ' ' + responsavel.get_nome() + ' PODE RETIRAR A CHAVE ' + mudar_cor(self.buscar_chave(local).get_local(), 32)), 34))
            chaveDAO.retirar_chave(local, self.data_atual(), self.hora_atual(), '-----', matricula_responsavel)
        elif self.chave_livre(local) == False:
            print(mudar_cor('\nESTA CHAVE FOI RETIRADA POR ' + mudar_cor(self.buscar_responsavel(self.buscar_chave_em_circulacao(local).get_responsavel()).get_nome(), 31), 34))
            print(self.buscar_chave_em_circulacao(local))

    def devolver_chave(self, local, matricula_responsavel):
        chave = self.buscar_chave_em_circulacao(local)
        responsavel = self.buscar_responsavel(matricula_responsavel)
        if chave == None:
            print(mudar_cor('\nESTA CHAVE NÃO FOI RETIRADA, PARA QUE POSSA SER DEVOLVIDA', 31))
        else:
            print(mudar_cor(('\nO ' + responsavel.get_tipo() + ' ' + responsavel.get_nome() + ' PODE DEVOLVER A CHAVE ' + mudar_cor(self.buscar_chave(local).get_local(), 32)), 34))
            horario_chegada = self.hora_atual()
            chaveDAO.devolver_chave(chave.get_local(), horario_chegada)

    def buscar_chave(self, local):
        chave = chaveDAO.buscar_chave(local)
        if chave != None:
            return chave

    def buscar_chave_em_circulacao(self, local):
        chave = chaveDAO.buscar_chave_circulacao(local)
        if chave != None:
            return chave

    def buscar_chave_responsavel(self, matricula):
        chave = chaveDAO.buscar_chave_com_responsavel(matricula)
        if chave != None:
            return chave

    def chaves_em_circulacao(self):
        return chaveDAO.chaves_em_circulacao()

    def chaves_disponiveis(self):
        lista_em_circulacao = chaveDAO.chaves_em_circulacao()
        lista_geral = chaveDAO.chaves_em_geral()
        lista_chaves_livres = []
        for chave in lista_geral:
            if chave not in lista_em_circulacao:
                lista_chaves_livres.append(chave)
        return lista_chaves_livres

    def chave_livre(self, local):
        if self.buscar_chave(local) != None:
            if self.buscar_chave_em_circulacao(local) == None:
                return True
            else:
                return False
        else:
            return None

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

#---------------    MEMORANDO    -----------------

    def cadastrar_memorando(self, professor, lista_alunos, inicio, encerramento):
        for aluno in lista_alunos:
            memorandoDAO.cadastrar_memorando(professor, aluno, inicio, encerramento)

    def validar_memorando(self):
        lista_memorandos = []
        for memorando in lista_memorandos:
            if memorando.get_situcao() == True:
                return True


#------------------    MENU    -------------------

    def menu_inicial(self):
        print(mudar_cor('\n ----------     RETIRAR CHAVES     ---------- ',34))
        print(mudar_cor('\n             Digite Sua Matricula ',34))
        matricula = input('                  ')
        responsavel = self.buscar_responsavel(matricula)
        if responsavel != None:
            opcao2=''
            while opcao2 != 'x':
                opcao2 = self.menu_2(responsavel)
        else:
            print(mudar_cor('\n            Matricula Não Conhecida', 31))
        return 'x'

    def menu_2(self, responsavel):
        if responsavel == 'manutenção':
            None
        else:
            tipo = self.analizar_tipo(responsavel)
            if tipo == True:
                self.menu_3(responsavel)
            else:
                self.menu_3(responsavel)
        return 'x'

    def menu_3(self, responsavel):
        print('O que deseja fazer? ')
        print('1 - Retirar Chave')
        print('2 - Devolver Chave')
        opcao = input('Opção Desejada: ')

        if opcao == '1':
            local = input('Digite o local no qual a chave se refere: ')
            self.retirar_chave(local.upper(), responsavel.get_matricula())

        elif opcao == '2':
            local = input('Digite o local no qual a chave se refere: ')
            self.devolver_chave(local.upper(), responsavel.get_matricula())




