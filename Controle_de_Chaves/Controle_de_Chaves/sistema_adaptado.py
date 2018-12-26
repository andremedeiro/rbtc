from chaveDAO import ChaveDAO
from usuarioDAO import UsuarioDAO
from memorandoDAO import MemorandoDAO
from chave import Chave
from usuario import Usuario
from memorando import Memorando
from datetime import datetime
from tkinter import *
import sqlite3

def mudar_cor(texto, cor):
    return str('\033[' + str(cor) + 'm' + str(texto) + '\033[0;0m')

conexao = sqlite3.connect("Controle_de_Chave.db")

usuarioDAO=UsuarioDAO()
chaveDAO=ChaveDAO()
memorandoDAO=MemorandoDAO()

class Sistema:

    def __init__(self, interface):
        self.criar_tabela()
        self.senha = 'ADMIN'
        self.matricula_administrador = 'ADMIN'
        self.interface=interface

    def criar_tabela(self):
        cursor = conexao.cursor()
        cursor.execute('create table if not exists administrador(matricula text, senha text)')
        cursor.close()

    def inserir(self):
        cursor = conexao.cursor()
        cursor.execute('insert into administrador values(?,?)', (self.matricula_administrador, self.senha))
        conexao.commit()
        cursor.close()

    def alterar_senha(self, novo):
        cursor = conexao.cursor()
        try:
            cursor.execute('update administrador set senha = ? where senha = ?',(novo, self.senha))
            conexao.commit()
            cursor.close()
        except:
            return False
        else:
            return True


    def alterar_matricula_admin(self, novo):
        cursor = conexao.cursor()
        try:
            cursor.execute('update administrador set matricula = ? where matricula = ?',(novo, self.matricula_administrador))
            conexao.commit()
            cursor.close()
        except:
            return False
        else:
            return True


    def get_matricula_administrador(self):
        return self.matricula_administrador

    def get_senha(self):
        return self.senha

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

    def erro(self, texto):
        erro=self.interface.erro
        erro.pack_forget()
        erro['text']=texto
        erro.pack()

    def aviso(self, texto):
        aviso=self.interface.aviso
        aviso.pack_forget()
        aviso['text']=texto
        aviso.pack()




# ____________________    CHAVE   ________________________

    def cadastrar_chave(self, local):
        try:
            chaveDAO.insere_chave(local)
        except:
            return False
        else:
            return True

    def retirar_chave(self, local, usuario):
        if self.buscar_chave(local.upper()) != None:
            chave_em_circulacao=self.buscar_chave_circulacao(local.upper())
            if chave_em_circulacao == None:
                if usuario.get_tipo() == 'DISCENTE':
                    if self.buscar_autorizacao(usuario.get_matricula(), local.upper()) != None:
                        try:
                            chaveDAO.retira_chave(local.upper(), usuario.get_matricula())
                        except:
                            self.erro('Erro no Banco de Dados')
                        else:
                            self.aviso('A Chave {} pode ser retirada por {}'.format(local.upper(), usuario.get_nome()))
                    else:
                        self.erro('O Discente {} não está autorizado a retirar a chave {}'.format(usuario.get_nome(), local.upper()))
                else:
                    try:
                        chaveDAO.retira_chave(local.upper(), usuario.get_matricula())
                    except:
                        self.erro('Erro no Banco de Dados')
                    else:
                        self.aviso('A Chave {} pode ser retirada por {}'.format(local.upper(), usuario.get_nome()))
            else:
                self.aviso('A chave {} foi retirada por {}'.format(local.upper(), self.buscar_usuario(chave_em_circulacao.get_usuario_retirada()).get_nome()))

        else:
            self.erro('A Chave {} não existe'.format(local))


    def devolver_chave(self, local, usuario):
        if self.buscar_chave(local.upper()) != None:
            chave_em_circulacao=self.buscar_chave_circulacao(local.upper())
            if chave_em_circulacao != None:
                try:
                    autorizacao = self.buscar_autorizacao(usuario.get_matricula(), local)
                    chaveDAO.devolve_chave(local, usuario.get_matricula())
                except:
                    self.erro('Erro no Banco de Dados')
                else:
                    if autorizacao == True:
                        self.aviso('A Chave {} pode ser devolvida por {}'.format(local.upper(), usuario.get_nome()))
                    else:
                        self.erro('{} não tem autorização para transitar com a chave {}, mas houve a devolução'.format(usuario.get_nome(),local.upper()))
            else:
                self.erro('A chave {} não foi retirada'.format(local.upper()))
        else:
            self.erro('A chave {} não existe'.format(local.upper()))

    def buscar_chave(self, local):
        chave = chaveDAO.buscar_chave(local)
        if chave != None:
            return chave

    def buscar_chave_circulacao(self, local):
        for chave in chaveDAO.chaves_em_circulacao():
            if chave.get_local() == local:
                return chave

    def remover_chave(self, local):
        try:
            chaveDAO.remover_chave(local)
        except:
            return False
        else:
            return True


    def listar_chaves(self):
        lista=chaveDAO.listar_chaves()
        if len(lista) != 0:
            return lista
        else:
            return False

    def chaves_em_circulacao(self):
        lista=chaveDAO.chaves_em_circulacao()
        if len(lista) != 0:
            return lista
        else:
            return False

# ____________________    USUARIO   ________________________

    def cadastrar_usuario(self, nome, matricula, tipo):
        try:
            usuarioDAO.insere_usuario(nome, matricula, tipo)
        except:
            return False
        else:
            return True

    def buscar_usuario(self, matricula):
        if matricula == self.matricula_administrador:
            return 'ADMINISTRADOR'
        else:
            return usuarioDAO.buscar_usuario(matricula)

    def remover_usuario(self, matricula):
        try:
            usuario = self.buscar_usuario(matricula)
            usuarioDAO.remove_usuario(matricula)
        except:
            return False
        else:
            return True

    def listar_usuarios(self):
        lista=usuarioDAO.listar_usuarios()
        if len(lista) != 0:
            return lista
        else:
            return False

# ____________________    MEMORANDO   ________________________

    def cadastrar_memorando(self, local, professor, alunos, inicio, encerramento):
        try:
            for aluno in alunos:
                usuario = self.buscar_usuario(aluno)
                if usuario == None:
                    return False
                else:
                    memorandoDAO.insere_memorando(local, professor, aluno, inicio, encerramento)
        except:
            return False
        else:
            return True

    def buscar_autorizacao(self, matricula, local):
        return memorandoDAO.buscar_autorizacao(matricula, local)

    def listar_memorandos(self):
        lista = memorandoDAO.listar_memorandos()
        if len(lista) != 0:
            return lista
        else:
            return False

    def memorandos_validos(self):
        lista = memorandoDAO.memorando_validos()
        if len(lista) != 0:
            return lista
        else:
            return False

#____________________    MENU   ________________________

    # def menu_principal(self):
    #     print(mudar_cor('\n-'+'-'*9+' '*8+"CONTROLE DE CHAVES"+' '*8+'-'*10, 34))
    #     matricula = str(input(mudar_cor('\nDIGITE SUA MATRICULA: ',34))).upper()
    #     opcao = ''
    #     usuario = self.buscar_usuario(matricula)
    #     if usuario == 'ADMINISTRADOR':
    #         senha = input('\nDIGITE A SENHA PARA ENTRAR COMO ADMINISTRADOR: ').upper()
    #         if senha == self.senha:
    #             while opcao != 'X':
    #                 opcao = self.menu_administrador()
    #         else:
    #             print(mudar_cor('\nSENHA DESCONHECIDA', 31))
    #     else:
    #         if usuario == None:
    #             print(mudar_cor('\nUSUÁRIO DESCONHECIDO', 31))
    #         else:
    #             self.menu_usuario(usuario)
    #     return matricula
    #
    # def menu_usuario(self, usuario):
    #     print(mudar_cor('\n-' + '-' * 12 + ' ' * 8 + "MENU USUÁRIO" + ' ' * 8 + '-' * 13, 32))
    #     print('\nO QUE DESEJA FAZER {}? '.format(usuario.get_nome()))
    #     print(mudar_cor('\n1', 34) + ' - RETIRAR CHAVE    |' + mudar_cor(' 2', 34) + ' - DEVOLVER CHAVE')
    #     print(mudar_cor(' '*15+'X', 31) + ' - SAIR')
    #     opcao = input('\nOPÇÃO DESEJADA: ').upper()
    #
    #     if opcao == '1':
    #         print(mudar_cor('\n-' + '-' * 12 + ' ' * 7 + "RETIRAR CHAVE" + ' ' * 8 + '-' * 13, 32))
    #         local = input('\nDIGITE O LOCAL NO QUAL A CHAVE SE REFERE: ').upper()
    #         if self.buscar_chave(local) != None:
    #             chave = self.buscar_chave_circulacao(local)
    #             if chave == None:
    #                 if usuario.get_tipo() == 'DISCENTE':
    #                     if self.buscar_autorizacao(usuario.get_matricula(), local.upper()) != None:
    #                         self.retirar_chave(local.upper(), usuario)
    #                     else:
    #                         print(mudar_cor("DISCENTE NÃO AUTORIZADO PARA RETIRAR ESTA CHAVE", 31))
    #                 else:
    #                     self.retirar_chave(local.upper(), usuario)
    #             else:
    #                 usuario = self.buscar_usuario(chave.get_usuario_retirada())
    #                 print(mudar_cor('\nA CHAVE JÁ FOI RETIRADA POR: {}'.format(usuario), 34))
    #                 print(chave)
    #         else:
    #             print(mudar_cor('\nCHAVE NÃO EXISTE', 31))
    #
    #     elif opcao == '2':
    #         print(mudar_cor('\n-' + '-' * 11 + ' ' * 8 + "DEVOLVER CHAVE" + ' ' * 8 + '-' * 12, 32))
    #         local = input('\nDIGITE O LOCAL NO QUAL A CHAVE SE REFERE: '.upper()).upper()
    #         if self.buscar_chave(local) != None:
    #             if self.buscar_chave_circulacao(local) != None:
    #                 self.devolver_chave(local.upper(), usuario)
    #             else:
    #                 print(mudar_cor('\nESTA CHAVE NÃO FOI RETIRADA', 31))
    #         else:
    #             print(mudar_cor('\nCHAVE NÃO EXISTE', 31))
    #
    #     elif opcao == 'X':
    #         None
    #
    #     else:
    #         print(mudar_cor('\nOPÇÃO NÃO ENCONTRADA', 31))
    #
    # def menu_administrador(self):
    #     print(mudar_cor('\n-'+'-'*9+' '*8+"MENU ADMINISTRADOR"+' '*8+'-'*10, 31))
    #     print(mudar_cor('\n1',34)+' - CADASTRAR USUÁRIO    |'+mudar_cor(' 7',34)+' - REMOVER USUÁRIO')
    #     print(mudar_cor('2',34)+' - CADASTRAR CHAVE      |'+mudar_cor(' 8',34)+' - REMOVER CHAVE')
    #     print(mudar_cor('3',34)+' - CADASTRAR MEMORANDO  |'+mudar_cor(' 9',34)+' - EDITAR MATRICULA OU SENHA DE ADMINISTRADOR')
    #     print(mudar_cor('4',34)+' - LISTAR USUÁRIOS      |'+mudar_cor(' 10',34)+' - LISTAR CHAVES')
    #     print(mudar_cor('5',34)+' - LISTAR MEMORANDOS    |'+mudar_cor(' 11',34)+' - LISTAR APENAS MEMORANDOS VÁLIDOS')
    #     print(mudar_cor('6',34)+' - CHAVES EM CIRCULAÇÃO |')
    #     print(mudar_cor(' ' * 20 + 'X', 31) + ' - SAIR')
    #     opcao=input('\nDIGITE A OPÇÃO DESEJADA: ').upper()
    #
    #     if opcao == '1':
    #         print(mudar_cor('\n ' + ' ' * 11 + ' ' * 8 +'CADASTRAR USUÁRIO', 34))
    #         nome = input('\nNOME: ').upper()
    #         matricula = input('MATRICULA: ').upper()
    #         usuario = self.buscar_usuario(matricula)
    #         if usuario == None:
    #             if len(matricula) == 11 or len(matricula) == 12:
    #                 self.cadastrar_usuario(nome.upper(), matricula.upper(), 'DISCENTE')
    #             elif len(matricula) == 7:
    #                 self.cadastrar_usuario(nome.upper(), matricula.upper(), 'DOCENTE')
    #             else:
    #                 print(mudar_cor('\n{} NÃO É UMA MATRICULA RECONHECIDA'.format(matricula), 31))
    #         else:
    #             print(mudar_cor('\nJÁ EXISTE UM USUÁRIO COM ESTA MATRICULA',31))
    #             print(usuario)
    #
    #     elif opcao == '2':
    #         print(mudar_cor('\n ' + ' ' * 11 + ' ' * 8 +'CADASTRAR CHAVE', 34))
    #         local=input('\nLOCAL NO QUAL A CHAVE SE REFERE: ').upper()
    #         chave=self.buscar_chave(local.upper())
    #         if chave == None:
    #             self.cadastrar_chave(local)
    #         else:
    #             print(mudar_cor('\nCHAVE JÀ EXISTENTE', 31))
    #             print(chave)
    #
    #     elif opcao == '3':
    #         print(mudar_cor('\n ' + ' ' * 11 + ' ' * 8 +'CADASTRAR MEMORANDO', 34))
    #         local=input('\nLOCAL NO QUAL OS ALUNOS TERÃO ACESSO: ').upper()
    #         local=self.buscar_chave(local)
    #         if local != None:
    #             professor=input('MATRICULA DO DOCENTE QUE CONCEDERÁ O ACESSO: ')
    #             professor=self.buscar_usuario(professor)
    #             if professor == None:
    #                 print(mudar_cor('NÃO FOI ENCONTRADO NENHUM DOCENTE COM ESTA MATRICULA', 31))
    #             else:
    #                 alunos=input('MATRICULAS DOS ALUNOS'+mudar_cor(' (SEPARADOS POR /): ',34)).split('/')
    #                 encerramento=input('ATÉ QUANDO ESTE USUÁRIO TERÁ VALIDADE?'+mudar_cor(' INSIRA A DATA DESTA FORMA: [DD/MM/AAAA] ', 34))
    #                 self.cadastrar_memorando(local.get_local(),professor.get_matricula(), alunos, self.data_atual(), encerramento)
    #         else:
    #             print(mudar_cor('\nNÃO HÁ CHAVE REFERENTE A ESTE LOCAL',31))
    #
    #     elif opcao == '4':
    #         self.listar_usuarios()
    #
    #     elif opcao == '5':
    #         self.listar_memorandos()
    #
    #     elif opcao == '6':
    #         self.chaves_em_circulacao()
    #
    #     elif opcao == '7':
    #         print(mudar_cor('\n ' + ' ' * 11 + ' ' * 8 +'REMOVER USUÁRIO', 31))
    #         matricula=input('\nMATRICULA DO USUÁRIO A SER REMOVIDO: ').upper()
    #         usuario = self.buscar_usuario(matricula)
    #         if usuario != None:
    #             certeza=input('\nCERTEZA QUE DESEJA EXCLUIR: {} [sim/nao]'.format(usuario)).upper()
    #             if certeza == 'SIM':
    #                 self.remover_usuario(usuario.get_matricula())
    #         else:
    #             print(mudar_cor('\nNÃO FOI ENCONTRADO NENHUM USUÁRIO COM A MATRICULA {}'.format(matricula), 31))
    #
    #     elif opcao == '8':
    #         print(mudar_cor('\n ' + ' ' * 11 + ' ' * 8 +'REMOVER CHAVE', 31))
    #         local = input('\nLOCAL NO QUAL A CHAVE A SER REMOVIDA SE REFERE: ').upper()
    #         chave = self.buscar_chave(local)
    #         if chave != None:
    #             certeza = input('\nCERTEZA QUE DESEJA EXCLUIR A CHAVE: {} [sim/nao]'.format(chave)).upper()
    #             if certeza == 'SIM':
    #                 self.remover_chave(chave.get_local())
    #         else:
    #             print(mudar_cor('\nNÃO FOI ENCONTRADO NENHUMA CHAVE REFERENTE AO LOCAL {}'.format(chave), 31))
    #
    #     elif opcao == '9':
    #         print(mudar_cor('\n ' + ' ' * 11 + ' ' * 8 +'EDITAR ADMINISTRADOR',34))
    #         print(mudar_cor('\n1', 34) + ' - ALTERAR SENHA    |' + mudar_cor(' 2', 34) + ' - ALTERAR MATRICULA')
    #         opcao = input('\nO QUE DESEJA ALTERAR? ')
    #
    #         if opcao == '1':
    #             print(mudar_cor('\n ' + ' ' * 11 + ' ' * 8 + 'ALTERAR SENHA', 34))
    #             senha1 = input(mudar_cor('NOVA SENHA: ', 34)).upper()
    #             senha2 = input(mudar_cor('CONFIRME A SENHA: ', 34)).upper()
    #             while self.senha == None:
    #                 if senha1 != senha2:
    #                     print(mudar_cor("\nSENHAS NÃO COINCIDEM", 31))
    #                     senha1 = input(mudar_cor('NOVA SENHA: ', 34)).upper()
    #                     senha2 = input(mudar_cor('CONFIRME A SENHA: ', 34)).upper()
    #                 else:
    #                     self.alterar_senha(senha1)
    #                     self.senha = senha1
    #                     self.gerar_matricula()
    #                     print(mudar_cor("SENHA CADASTRADA", 32))
    #                     print(mudar_cor(
    #                         "Matricula do Administrardor: {}| Senha adminitrado: {}".format(self.matricula_administrador,
    #                                                                                        self.senha), 34))
    #
    #         elif opcao == '2':
    #             print(mudar_cor('\n ' + ' ' * 11 + ' ' * 8 + 'ALTERAR MATRICULA', 34))
    #             nova_matricula=input('\nNOVA MATRICULA: ').upper()
    #             self.alterar_matricula_admin(nova_matricula)
    #             self.matricula_administrador = nova_matricula
    #             self.gerar_matricula()
    #             print(mudar_cor("NOVA MATRICULA CADASTRADA", 32))
    #             print(mudar_cor(
    #                 "Matricula do Administrardor: {}| Senha adminitrado: {}".format(self.matricula_administrador,
    #                                                                                 self.senha), 34))
    #
    #         else:
    #             print(mudar_cor('OPÇÃO NÃO ENCONTRADA', 31))
    #
    #     elif opcao == '10':
    #         self.listar_chaves()
    #
    #     elif opcao == '11':
    #         self.memorandos_validos()
    #
    #     elif opcao == 'X':
    #         return opcao
    #
    #     else:
    #         print(mudar_cor('\nOPÇÃO NÃO ENCONTRADA', 31))
    #
    #     return opcao






