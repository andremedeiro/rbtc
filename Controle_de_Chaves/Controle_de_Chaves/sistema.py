from chaveDAO import ChaveDAO
from usuarioDAO import UsuarioDAO
from memorandoDAO import MemorandoDAO
from chave import Chave
from usuario import Usuario
from memorando import Memorando
from datetime import datetime
import sqlite3

def mudar_cor(texto, cor):
    return str('\033[' + str(cor) + 'm' + str(texto) + '\033[0;0m')

conexao = sqlite3.connect("Controle_de_Chave.db")

usuarioDAO=UsuarioDAO()
chaveDAO=ChaveDAO()
memorandoDAO=MemorandoDAO()

class Sistema:

    def __init__(self):
        self.criar_tabela()
        self.senha = None
        self.matricula_administrador = None
        self.matricula_administrador = self.gerar_matricula()

    def gerar_matricula(self):
        cursor=conexao.cursor()
        for tupla in cursor.execute('select count(*) from administrador'):
            quantidade = tupla[0]
        if quantidade == 0:
            print("-"*10+' '*8+"CADASTRAR ADMINISTRADOR"+' '*8+'-'*10)
            matricula=input(mudar_cor("Matricula Administrador: ", 34)).upper()
            self.matricula_administrador = matricula
            senha1=input(mudar_cor('Senha de Administrador: ',34)).upper()
            senha2=input(mudar_cor('Confirme a senha: ', 34)).upper()
            while self.senha == None:
                if senha1 != senha2:
                    print(mudar_cor("\nSenhas não coincidem",31))
                    senha1 = input(mudar_cor('Senha de Administrador: ', 34)).upper()
                    senha2 = input(mudar_cor('Confirme a senha: ', 34)).upper()
                else:
                    self.senha = senha1
                    print(mudar_cor("Senha Cadastrada", 32))
                    print(mudar_cor("Matricula do Admiistrardor: {}| Senha adminitrado: {}".format(self.matricula_administrador, self.senha), 34))
            self.inserir()
        else:
            for tupla in cursor.execute('select * from administrador'):
                if tupla != None:
                    self.matricula_administrador = tupla[0]
                    self.senha=tupla[1]
            # matricula=input(mudar_cor("\nPARA INICIAR O SOFTWARE DIGITE A MATRICULA DO ADMINISTRADOR: ", 34)).upper()
            matricula = self.matricula_administrador
            if matricula == self.matricula_administrador:
                senha=self.senha
                # senha=input(mudar_cor('\nSENHA DE ADMINISTRADOR: ', 34)).upper()
                if senha == self.senha:
                    opcao = ''
                    while opcao != 'X':
                        opcao = self.menu_principal()
                else:
                    print(mudar_cor('\nSENHA INCORRETA', 31))
            else:
                print(mudar_cor("\nMATRICULA INCORRETA", 31))
        cursor.close()

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
        except:
            print(mudar_cor('\nDESCULPE, MAS HOUVE UM ERRO NA ALTERAÇÃO',31))
        else:
            print(mudar_cor('\nSENHA ALTERADA COM SUCESSO',32))
        cursor.close()

    def alterar_matricula_admin(self, novo):
        cursor = conexao.cursor()
        try:
            cursor.execute('update administrador set matricula = ? where matricula = ?',
                           (novo, self.matricula_administrador))
            conexao.commit()
        except:
            print(mudar_cor('\nDESCULPE, MAS HOUVE UM ERRO NA ALTERAÇÃO',31))
        else:
            print(mudar_cor('\nMATRICULA ALTERADA COM SUCESSO',32))
        cursor.close()

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

# ____________________    CHAVE   ________________________

    def cadastrar_chave(self, local):
        try:
            chaveDAO.insere_chave(local)
        except:
            print(mudar_cor("\nDESCULPE, MAS HOUVE UM ERRO NO CADASTRO DA CHAVE", 31))
        else:
            print(mudar_cor('\nCHAVE CADASTRADA COM SUCESSO', 32))

    def retirar_chave(self, local, usuario):
        try:
            chaveDAO.retira_chave(local, usuario.get_matricula())
        except:
            print(mudar_cor('\nDESCULPE, MAS HOUVE UM ERRO NA RETIRADA DA CHAVE', 31))
        else:
            print(mudar_cor('\nO(A) USUARIO(A) {} PODE RETIRAR A CHAVE DO(DA) {}'.format(usuario.get_nome(), mudar_cor(local,34)), 32))

    def devolver_chave(self, local, usuario):
        try:
            autorizacao = self.buscar_autorizacao(usuario.get_matricula(), local)
            chaveDAO.devolve_chave(local, usuario.get_matricula())
        except:
            print(mudar_cor('\nDESCULPE, MAS HOUVE UM ERRO NA DEVOLUÇÃO DA CHAVE', 31))
        else:
            if autorizacao == True:
                print(mudar_cor('\nO(A) USUARIO(A) {} PODE DEVOLVER A CHAVE DO(DA) {}'.format(usuario.get_nome(), mudar_cor(local,34)), 32))
            else:
                print(mudar_cor('\nO(A) USUÁRIO(A) {} NÃO TEM AUTORIZAÇÃO PARA TRANSITAR COM A CHAVE DO(DA) {}, MAS A DEVOLUÇÃO FOI FEITA'.format(usuario.get_nome(), local), 31))

    def buscar_chave(self, local):
        chave = chaveDAO.buscar_chave(local)
        if chave != None:
            return chave

    def buscar_chave_circulacao(self, local):
        for chave in chaveDAO.chaves_em_cirsulacao():
            if chave.get_local() == local:
                return chave

    def remover_chave(self, local):
        try:
            chaveDAO.remover_chave(local)
        except:
            print(mudar_cor('\nDESCULPE, MAS HOUVE UM ERRO NA EXCLUSÃO DA CHAVE', 31))
        else:
            print(mudar_cor('\nA CHAVE {} FOR REMOVIDA COM SUCESSO'.format(local), 32))


    def listar_chaves(self):
        lista=chaveDAO.listar_chaves()
        if len(lista) != 0:
            print('\nCHAVES EXITENTES: ')
            for chave in lista:
                print(chave)
        else:
            print(mudar_cor('\nNÃO HÁ NENHUMA CHAVE CADASTRADAS'))

    def chaves_em_circulacao(self):
        lista=chaveDAO.chaves_em_circulacao()
        if len(lista) != 0:
            print('\nCHAVES EM CIRCULAÇÃO:')
            for chave in lista:
                print(chave)
        else:
            print(mudar_cor('\nNÃO HÁ CHAVES EM CIRCULAÇÃO',31))

# ____________________    USUARIO   ________________________

    def cadastrar_usuario(self, nome, matricula, tipo):
        try:
            usuarioDAO.insere_usuario(nome, matricula, tipo)
        except:
            print(mudar_cor('\nDESCULPE, MAS HOUVE UM ERRO NA ADIÇÃO DO USUÁRIO', 31))
        else:
            print(mudar_cor('\nUSUÁRIO CADASTRADO COM SUCESSO', 32))

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
            print(mudar_cor("\nDESCULPE, MAS HOUVE UMA ERRO NA EXCLUSÃO", 31))
        else:
            print(mudar_cor('\nO(A)USUÁRIO(A) {} FOI REMOVIDA COM SUCESSO'.format(usuario.get_nome()), 32))

    def listar_usuarios(self):
        lista=usuarioDAO.listar_usuarios()
        if len(lista) != 0:
            print('\nUSUÁRIOS:')
            for usuario in lista:
                print(usuario)
        else:
            print(mudar_cor('\nNÃO HÁ NENHUM USUÁRIO CADASTRADO',31))

# ____________________    MEMORANDO   ________________________

    def cadastrar_memorando(self, local, professor, alunos, inicio, encerramento):
        try:
            for aluno in alunos:
                usuario = self.buscar_usuario(aluno)
                if usuario == None:
                    print(mudar_cor('NÃO FOI ENCONTRADO NENHUM USUÁRIO COM A MATRICULA {}, MAS PROSSEGUIREMOS COM O CADASTRO DA MESMA FORMA'.format(aluno), 31))
                else:
                    memorandoDAO.insere_memorando(local, professor, aluno, inicio, encerramento)
        except:
            print(mudar_cor('\nDESCULPE, MAS HOUVE UM ERRO NO CADASTRO DO MEMORANDO', 31))
        else:
            print(mudar_cor('\nMEMORANDO CADASTRADO COM SUCESSO',32))

    def buscar_autorizacao(self, matricula, local):
        return memorandoDAO.buscar_autorizacao(matricula, local)

    def listar_memorandos(self):
        print('\nOS MEMORANDO VÁLIDOS ESTÃO EM {} OS INVÁLIDOS ESTÃO EM {}'.format(mudar_cor('VERDE', 32),mudar_cor('VERMELHO',31)))
        for memorando in memorandoDAO.listar_memorandos():
            if memorando.get_situacao() == 'INVALIDO':
                print(mudar_cor(memorando,31))
            else:
                print(mudar_cor(memorando, 32))

    def memorandos_validos(self):
        print('\nMEMORANDOS VÁLIDOS: ')
        for memorando in memorandoDAO.memorando_validos():
            print(memorando)

#____________________    MENU   ________________________

    def menu_principal(self):
        print(mudar_cor('\n-'+'-'*9+' '*8+"CONTROLE DE CHAVES"+' '*8+'-'*10, 34))
        matricula = str(input(mudar_cor('\nDIGITE SUA MATRICULA: ',34))).upper()
        opcao = ''
        usuario = self.buscar_usuario(matricula)
        if usuario == 'ADMINISTRADOR':
            senha = input('\nDIGITE A SENHA PARA ENTRAR COMO ADMINISTRADOR: ').upper()
            if senha == self.senha:
                while opcao != 'X':
                    opcao = self.menu_administrador()
            else:
                print(mudar_cor('\nSENHA DESCONHECIDA', 31))
        else:
            if usuario == None:
                print(mudar_cor('\nUSUÁRIO DESCONHECIDO', 31))
            else:
                self.menu_usuario(usuario)
        return matricula

    def menu_usuario(self, usuario):
        print(mudar_cor('\n-' + '-' * 12 + ' ' * 8 + "MENU USUÁRIO" + ' ' * 8 + '-' * 13, 32))
        print('\nO QUE DESEJA FAZER {}? '.format(usuario.get_nome()))
        print(mudar_cor('\n1', 34) + ' - RETIRAR CHAVE    |' + mudar_cor(' 2', 34) + ' - DEVOLVER CHAVE')
        print(mudar_cor(' '*15+'X', 31) + ' - SAIR')
        opcao = input('\nOPÇÃO DESEJADA: ').upper()

        if opcao == '1':
            print(mudar_cor('\n-' + '-' * 12 + ' ' * 7 + "RETIRAR CHAVE" + ' ' * 8 + '-' * 13, 32))
            local = input('\nDIGITE O LOCAL NO QUAL A CHAVE SE REFERE: ').upper()
            if self.buscar_chave(local) != None:
                chave = self.buscar_chave_circulacao(local)
                if chave == None:
                    if usuario.get_tipo() == 'DISCENTE':
                        if self.buscar_autorizacao(usuario.get_matricula(), local.upper()) != None:
                            self.retirar_chave(local.upper(), usuario)
                        else:
                            print(mudar_cor("DISCENTE NÃO AUTORIZADO PARA RETIRAR ESTA CHAVE", 31))
                    else:
                        self.retirar_chave(local.upper(), usuario)
                else:
                    usuario = self.buscar_usuario(chave.get_usuario_retirada())
                    print(mudar_cor('\nA CHAVE JÁ FOI RETIRADA POR: {}'.format(usuario), 34))
                    print(chave)
            else:
                print(mudar_cor('\nCHAVE NÃO EXISTE', 31))

        elif opcao == '2':
            print(mudar_cor('\n-' + '-' * 11 + ' ' * 8 + "DEVOLVER CHAVE" + ' ' * 8 + '-' * 12, 32))
            local = input('\nDIGITE O LOCAL NO QUAL A CHAVE SE REFERE: '.upper()).upper()
            if self.buscar_chave(local) != None:
                if self.buscar_chave_circulacao(local) != None:
                    self.devolver_chave(local.upper(), usuario)
                else:
                    print(mudar_cor('\nESTA CHAVE NÃO FOI RETIRADA', 31))
            else:
                print(mudar_cor('\nCHAVE NÃO EXISTE', 31))

        elif opcao == 'X':
            None

        else:
            print(mudar_cor('\nOPÇÃO NÃO ENCONTRADA', 31))

    def menu_administrador(self):
        print(mudar_cor('\n-'+'-'*9+' '*8+"MENU ADMINISTRADOR"+' '*8+'-'*10, 31))
        print(mudar_cor('\n1',34)+' - CADASTRAR USUÁRIO    |'+mudar_cor(' 7',34)+' - REMOVER USUÁRIO')
        print(mudar_cor('2',34)+' - CADASTRAR CHAVE      |'+mudar_cor(' 8',34)+' - REMOVER CHAVE')
        print(mudar_cor('3',34)+' - CADASTRAR MEMORANDO  |'+mudar_cor(' 9',34)+' - EDITAR MATRICULA OU SENHA DE ADMINISTRADOR')
        print(mudar_cor('4',34)+' - LISTAR USUÁRIOS      |'+mudar_cor(' 10',34)+' - LISTAR CHAVES')
        print(mudar_cor('5',34)+' - LISTAR MEMORANDOS    |'+mudar_cor(' 11',34)+' - LISTAR APENAS MEMORANDOS VÁLIDOS')
        print(mudar_cor('6',34)+' - CHAVES EM CIRCULAÇÃO |')
        print(mudar_cor(' ' * 20 + 'X', 31) + ' - SAIR')
        opcao=input('\nDIGITE A OPÇÃO DESEJADA: ').upper()

        if opcao == '1':
            print(mudar_cor('\n ' + ' ' * 11 + ' ' * 8 +'CADASTRAR USUÁRIO', 34))
            nome = input('\nNOME: ').upper()
            matricula = input('MATRICULA: ').upper()
            usuario = self.buscar_usuario(matricula)
            if usuario == None:
                if len(matricula) == 11 or len(matricula) == 12:
                    self.cadastrar_usuario(nome.upper(), matricula.upper(), 'DISCENTE')
                elif len(matricula) == 7:
                    self.cadastrar_usuario(nome.upper(), matricula.upper(), 'DOCENTE')
                else:
                    print(mudar_cor('\n{} NÃO É UMA MATRICULA RECONHECIDA'.format(matricula), 31))
            else:
                print(mudar_cor('\nJÁ EXISTE UM USUÁRIO COM ESTA MATRICULA',31))
                print(usuario)

        elif opcao == '2':
            print(mudar_cor('\n ' + ' ' * 11 + ' ' * 8 +'CADASTRAR CHAVE', 34))
            local=input('\nLOCAL NO QUAL A CHAVE SE REFERE: ').upper()
            chave=self.buscar_chave(local.upper())
            if chave == None:
                self.cadastrar_chave(local)
            else:
                print(mudar_cor('\nCHAVE JÀ EXISTENTE', 31))
                print(chave)

        elif opcao == '3':
            print(mudar_cor('\n ' + ' ' * 11 + ' ' * 8 +'CADASTRAR MEMORANDO', 34))
            local=input('\nLOCAL NO QUAL OS ALUNOS TERÃO ACESSO: ').upper()
            local=self.buscar_chave(local)
            if local != None:
                professor=input('MATRICULA DO DOCENTE QUE CONCEDERÁ O ACESSO: ')
                professor=self.buscar_usuario(professor)
                if professor == None:
                    print(mudar_cor('NÃO FOI ENCONTRADO NENHUM DOCENTE COM ESTA MATRICULA', 31))
                else:
                    alunos=input('MATRICULAS DOS ALUNOS'+mudar_cor(' (SEPARADOS POR /): ',34)).split('/')
                    encerramento=input('ATÉ QUANDO ESTE USUÁRIO TERÁ VALIDADE?'+mudar_cor(' INSIRA A DATA DESTA FORMA: [DD/MM/AAAA] ', 34))
                    self.cadastrar_memorando(local.get_local(),professor.get_matricula(), alunos, self.data_atual(), encerramento)
            else:
                print(mudar_cor('\nNÃO HÁ CHAVE REFERENTE A ESTE LOCAL',31))

        elif opcao == '4':
            self.listar_usuarios()

        elif opcao == '5':
            self.listar_memorandos()

        elif opcao == '6':
            self.chaves_em_circulacao()

        elif opcao == '7':
            print(mudar_cor('\n ' + ' ' * 11 + ' ' * 8 +'REMOVER USUÁRIO', 31))
            matricula=input('\nMATRICULA DO USUÁRIO A SER REMOVIDO: ').upper()
            usuario = self.buscar_usuario(matricula)
            if usuario != None:
                certeza=input('\nCERTEZA QUE DESEJA EXCLUIR: {} [sim/nao]'.format(usuario)).upper()
                if certeza == 'SIM':
                    self.remover_usuario(usuario.get_matricula())
            else:
                print(mudar_cor('\nNÃO FOI ENCONTRADO NENHUM USUÁRIO COM A MATRICULA {}'.format(matricula), 31))

        elif opcao == '8':
            print(mudar_cor('\n ' + ' ' * 11 + ' ' * 8 +'REMOVER CHAVE', 31))
            local = input('\nLOCAL NO QUAL A CHAVE A SER REMOVIDA SE REFERE: ').upper()
            chave = self.buscar_chave(local)
            if chave != None:
                certeza = input('\nCERTEZA QUE DESEJA EXCLUIR A CHAVE: {} [sim/nao]'.format(chave)).upper()
                if certeza == 'SIM':
                    self.remover_chave(chave.get_local())
            else:
                print(mudar_cor('\nNÃO FOI ENCONTRADO NENHUMA CHAVE REFERENTE AO LOCAL {}'.format(chave), 31))

        elif opcao == '9':
            print(mudar_cor('\n ' + ' ' * 11 + ' ' * 8 +'EDITAR ADMINISTRADOR',34))
            print(mudar_cor('\n1', 34) + ' - ALTERAR SENHA    |' + mudar_cor(' 2', 34) + ' - ALTERAR MATRICULA')
            opcao = input('\nO QUE DESEJA ALTERAR? ')

            if opcao == '1':
                print(mudar_cor('\n ' + ' ' * 11 + ' ' * 8 + 'ALTERAR SENHA', 34))
                senha1 = input(mudar_cor('NOVA SENHA: ', 34)).upper()
                senha2 = input(mudar_cor('CONFIRME A SENHA: ', 34)).upper()
                while self.senha == None:
                    if senha1 != senha2:
                        print(mudar_cor("\nSENHAS NÃO COINCIDEM", 31))
                        senha1 = input(mudar_cor('NOVA SENHA: ', 34)).upper()
                        senha2 = input(mudar_cor('CONFIRME A SENHA: ', 34)).upper()
                    else:
                        self.alterar_senha(senha1)
                        self.senha = senha1
                        self.gerar_matricula()
                        print(mudar_cor("SENHA CADASTRADA", 32))
                        print(mudar_cor(
                            "Matricula do Administrardor: {}| Senha adminitrado: {}".format(self.matricula_administrador,
                                                                                           self.senha), 34))

            elif opcao == '2':
                print(mudar_cor('\n ' + ' ' * 11 + ' ' * 8 + 'ALTERAR MATRICULA', 34))
                nova_matricula=input('\nNOVA MATRICULA: ').upper()
                self.alterar_matricula_admin(nova_matricula)
                self.matricula_administrador = nova_matricula
                self.gerar_matricula()
                print(mudar_cor("NOVA MATRICULA CADASTRADA", 32))
                print(mudar_cor(
                    "Matricula do Administrardor: {}| Senha adminitrado: {}".format(self.matricula_administrador,
                                                                                    self.senha), 34))

            else:
                print(mudar_cor('OPÇÃO NÃO ENCONTRADA', 31))

        elif opcao == '10':
            self.listar_chaves()

        elif opcao == '11':
            self.memorandos_validos()

        elif opcao == 'X':
            return opcao

        else:
            print(mudar_cor('\nOPÇÃO NÃO ENCONTRADA', 31))

        return opcao






