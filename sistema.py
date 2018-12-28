from chaveDAO import ChaveDAO
from usuarioDAO import UsuarioDAO
from memorandoDAO import MemorandoDAO
from tkinter import *
import sqlite3
import time

def mudar_cor(texto, cor):
    return str('\033[' + str(cor) + 'm' + str(texto) + '\033[0;0m')

conexao = sqlite3.connect("Controle_de_Chave.db")

usuarioDAO=UsuarioDAO()
chaveDAO=ChaveDAO()
memorandoDAO=MemorandoDAO()

class Sistema:

    def __init__(self, interface):
        memorandoDAO.ajeitar_situacoes()
        self.criar_tabela()
        self.senha = None
        self.matricula_administrador = None
        self.interface=interface
        self.gerar_matricula()

    def gerar_matricula(self):
        cursor=conexao.cursor()
        for tupla in cursor.execute('select count(*) from administrador'):
            quantidade = tupla[0]
        if quantidade == 0:
            self.inserir()
        for tupla in cursor.execute('select * from administrador'):
            if tupla != None:
                self.matricula_administrador=tupla[0]
                self.senha=tupla[1]
        cursor.close()

    def criar_tabela(self):
        cursor = conexao.cursor()
        cursor.execute('create table if not exists administrador(matricula text, senha text)')
        cursor.close()

    def inserir(self):
        cursor = conexao.cursor()
        cursor.execute('insert into administrador values("ADMIN","ADMIN")')
        conexao.commit()
        cursor.close()

    def alterar_senha(self, senha1, senha2):
        if senha1 != senha2:
            self.erro('Senhas não Coincidem')
        else:
            cursor = conexao.cursor()
            try:
                cursor.execute('update administrador set senha = ? where senha = ?',(senha1, self.senha))
                conexao.commit()
                cursor.close()
            except:
                self.erro('Erro no Banco de Dados')
            else:
                self.senha=senha1
                self.aviso('Senha de Administrador Alterada')


    def alterar_matricula_admin(self, novo):
        cursor = conexao.cursor()
        try:
            cursor.execute('update administrador set matricula = ? where matricula = ?',(novo, self.matricula_administrador))
            conexao.commit()
            cursor.close()
        except:
            self.erro('Erro no Banco de Dados')
        else:
            self.matricula_administrador=novo
            self.aviso('Matricula de Administrador Alterada')


    def get_matricula_administrador(self):
        return self.matricula_administrador

    def get_senha(self):
        return self.senha

    def erro(self, texto):
        self.interface.aviso.pack_forget()
        erro=self.interface.erro
        erro.pack_forget()
        erro['text']=texto
        erro.pack()

    def aviso(self, texto):
        self.interface.erro.pack_forget()
        aviso=self.interface.aviso
        aviso.pack_forget()
        aviso['text']=texto
        aviso.pack()

    def listar(self,texto, lista):
        listagem=Tk()
        listagem.title(texto)
        listagem.geometry('1000x800')
        listagem.wm_iconbitmap('icone.ico')
        informe=Label(listagem, text=texto,font=['vernada','15','bold'],fg='grey')
        informe.pack()
        for coisa in lista:
            objeto=Label(listagem, text=coisa, font=['verdana', '8'])
            objeto.pack()
        listagem.mainloop()

# ____________________    CHAVE   ________________________

    def cadastrar_chave(self, local):
        chave=self.buscar_chave(local)
        if chave == None:
            try:
                chaveDAO.insere_chave(local)
            except:
                self.erro('Erro no Banco de Dados')
            else:
                self.aviso('Chave {} Cadastrada com Sucesso'.format(local))
        else:
            self.erro('Chave já Cadastrada')

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
        chave=self.buscar_chave(local)
        if chave != None:
            try:
                memorandoDAO.remove(local)
                chaveDAO.remover_chave(local)
            except:
                self.erro('Erro no Banco de Dados')
            else:
                self.aviso('Chave {} Removida'.format(chave.get_local()))
        else:
            self.erro('Não existe esta chave')


    def listar_chaves(self):
        lista=chaveDAO.listar_chaves()
        if len(lista) != 0:
            self.listar('Chaves:', lista)
        else:
            self.erro('Não Há Chaves Cadastradas')

    def chaves_em_circulacao(self):
        lista=chaveDAO.chaves_em_circulacao()
        if len(lista) != 0:
            self.listar('Chaves em Circulação:', lista)
        else:
            self.erro('Não Houve transito de chaves')

# ____________________    USUARIO   ________________________

    def cadastrar_usuario(self, nome, matricula):
        try:
            int(matricula)
        except:
            self.erro('Não pode haver letras em meio a matricula')
        else:
            usuario=self.buscar_usuario(matricula)
            if usuario == None:
                if len(matricula) == 11 or len(matricula) == 12:
                    try:
                        usuarioDAO.insere_usuario(nome, matricula, 'DISCENTE')
                    except:
                        self.erro('Erro no Banco de Dados')
                    else:
                        self.aviso('Usuário {} Cadastrado com Sucesso'.format(nome))
                elif len(matricula) == 7:
                    try:
                        usuarioDAO.insere_usuario(nome, matricula, 'DOCENTE')
                    except:
                        self.erro('Erro no Banco de Dados')
                    else:
                        self.aviso('Usuário {} Cadastrado com Sucesso'.format(nome))
                else:
                    self.erro('Matricula Não Reconhecida')
            else:
                self.erro('Esta matricula pertence a {}'.format(usuario.get_nome()))

    def buscar_usuario(self, matricula):
        return usuarioDAO.buscar_usuario(matricula)

    def remover_usuario(self, matricula):
        usuario =self.buscar_usuario(matricula)
        if usuario != None:
            try:
                memorandoDAO.remove(matricula)
                usuarioDAO.remove_usuario(matricula)
            except:
                self.erro('Erro no Banco de Dados')
            else:
                self.aviso('Usuário {} Removido'.format(usuario.get_nome()))
        else:
            self.erro('Usuário não existe')

    def listar_usuarios(self):
        lista=usuarioDAO.listar_usuarios()
        if len(lista) != 0:
            self.listar('Usuários:', lista)
        else:
            self.erro('Não Há Usuários Cadastrados')
# ____________________    MEMORANDO   ________________________

    def cadastrar_memorando(self, local, professor, alunos, encerramento):
        if self.buscar_chave(local) != None:
            usuario_professor=self.buscar_usuario(professor)
            if usuario_professor != None:
                if usuario_professor.get_tipo() == 'DOCENTE':
                    try:
                        data = time.strptime(encerramento, "%d/%m/%Y")
                    except:
                        self.erro('" {} " É um formato de data invalido'.format(encerramento))
                    else:
                        for aluno in alunos:
                            usuario = self.buscar_usuario(aluno)
                            if usuario == None:
                                self.erro('Não foi encontrado um aluno de matricula " {} "'.format(aluno))
                            else:
                                try:
                                    memorandoDAO.insere_memorando(local, professor, aluno, encerramento)
                                except:
                                    self.erro('Erro no Banco de Dados ao cadastrar " {} "'.format(aluno))
                                else:
                                    if alunos.index(aluno) == (len(alunos)-1):
                                        self.aviso('Memorando Cadastrado com sucesso')
                else:
                    self.erro('" {} " não é um professor'.format(usuario_professor.get_nome()))
            else:
                self.erro('Não há um docente com matricula " {} "'.format(professor))
        else:
            self.erro('Não há chave " {} "'.format(local))

    def buscar_autorizacao(self, matricula, local):
        return memorandoDAO.buscar_autorizacao(matricula, local)

    def listar_memorandos(self):
        lista = memorandoDAO.listar_memorandos()
        if len(lista) != 0:
            self.listar('Memorandos em Geral:', lista)
        else:
            self.erro('Não há Memorandos Cadastrados')

    def memorandos_validos(self):
        lista = memorandoDAO.listar_memorandos()
        lista_real=[]
        for memorando in lista:
            if memorando.get_situacao() == 'VALIDO':
                lista_real.append(memorando)
        if len(lista_real) != 0:
            self.listar('Memorandos Válidos:', lista_real)
        else:
            self.erro('Não há Memorandos Válidos')
