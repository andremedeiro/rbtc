from sistema import *

class Interface:

    def __init__(self,  container):
        self.principal=container
        self.tela_principal()

    def tela_principal(self):
        self.frame1 = Frame(self.principal, pady=120)
        self.frame2 = Frame(self.principal, pady=5)
        self.frame_menu = Frame(self.principal, pady=20)
        self.frame_acao=Frame(self.frame_menu, pady=10)
        self.frame_aviso=Frame(self.principal, pady=5)

        self.frame1.pack()
        self.frame2.pack()
        self.frame_menu.pack()
        self.frame_acao.pack()
        self.frame_aviso.pack(side='bottom')

        self.frame_menu['bg'] = cinza
        self.frame1['bg'] = cinza
        self.frame2['bg'] = cinza
        self.frame_aviso['bg'] = cinza
        self.frame_acao['bg'] = cinza


        self.erro=Label(self.frame_aviso, font=['verdana','10', 'bold'], fg=vermelho, bg=cinza)
        self.aviso=Label(self.frame_aviso, font=['verdana','10', 'bold'], fg=verde, bg=cinza)

        self.ir = PhotoImage(file='feito.ppm')
        self.voltar=PhotoImage(file='voltar.ppm')
        self.mais=PhotoImage(file='mais.ppm')
        self.excluir=PhotoImage(file='excluir.ppm')

        self.informe = Label(self.frame1, text='DIGITE SUA MATRICULA:', font=font_aviso, fg=verde, bg=cinza)
        self.informe.pack()

        subframe=Frame(self.frame2, bg=cinza)
        subframe.pack()

        self.matricula = Entry(subframe, width=50,bd=2, relief='groove', font=['verdana','10'])
        self.matricula.pack(side='left')

        self.lancar=Button(subframe, command=self.menu_principal, relief='flat', overrelief='flat', bg=cinza)
        self.lancar['image']= self.ir
        self.lancar.image = self.ir
        self.lancar.pack(side='left')


    def menu_principal(self):
        self.erro.pack_forget()
        if self.matricula.get().upper() == sistema.get_matricula_administrador():
            self.matricula['state']='disabled'
            self.lancar['state'] = 'disabled'
            informe=Label(self.frame2, text="Senha de Administrador:", fg=verde, font=font_aviso, bg=cinza)
            informe.pack()
            senha=Entry(self.frame2, relief='groove', font=['Verdana','10'], width=50, bd=2)
            senha.pack(side='left')
            self.botao=Button(self.frame2, command=lambda:self.menu_administrador(senha), relief='flat', overrelief='flat', bg=cinza)
            self.botao['image'] = self.ir
            self.botao.image = self.ir
            self.botao.pack(side='left')
        else:
            usuario = sistema.buscar_usuario(self.matricula.get().upper())
            if usuario != None:
                self.matricula['state']='disabled'
                self.lancar['state']='disabled'
                self.menu_usuario(usuario)
            else:
                self.matricula.delete(0, END)
                self.frame_menu['pady']=10
                self.erro['text'] = 'Usuário Desconhecido'
                self.erro.pack()

    def limpar_tela(self):
        self.frame1.pack_forget()
        self.frame2.pack_forget()
        self.frame_menu.pack_forget()
        self.frame_acao.pack_forget()
        self.frame_aviso.pack_forget()

    def encerrar(self):
        self.limpar_tela()
        self.tela_principal()

    def menu_administrador(self,senha):
        if senha.get().upper() == sistema.get_senha():
            senha['state']='disabled'
            self.botao['state']='disabled'
            self.frame1['pady'] = 0
            self.frame1.pack()
            divisao = Label(self.frame_menu, text='-' * 80, fg=cinza_escuro, font=font_aviso, bg=cinza)
            divisao.pack()
            voltar = Button(self.frame_menu, command=self.encerrar, bg=cinza, relief='flat', overrelief='flat')
            voltar['image'] = self.voltar
            voltar.image = self.voltar
            voltar.pack(side='left')

            informe=Label(self.frame_menu, text='Menu Administrador', bg=cinza, fg=cinza_escuro, font=font_aviso)
            informe.pack()

            lista_acoes=['Cadastrar Usuário','Cadastrar Chave', 'Cadastrar Memorando','Listar Usuários', 'Listar Chaves', 'Listar Memorandos', 'Remover Usuário','Remover Chave','Memorandos Válidos', 'Chaves Em Circulação','Alterar Matricula Admin', 'Alterar Senha Admin']
            lista_funcoes=[lambda:self.cadastrar_usuario(),lambda:self.cadastrar_chave(), lambda:self.cadastrar_memorando(), lambda:sistema.listar_usuarios(), lambda:sistema.listar_chaves(), lambda:sistema.listar_memorandos(), lambda:self.remover_usuario(), lambda:self.remover_chave(), lambda:sistema.memorandos_validos(), lambda:sistema.chaves_em_circulacao(), lambda:self.alterar_matricula(), lambda:self.alterar_senha()]
            for indice in range(0,len(lista_acoes)):
                if indice % 3 == 0:
                    subframe=Frame(self.frame_menu, bg=cinza, pady=2)
                    subframe.pack()
                botao=Button(subframe, text=lista_acoes[indice],command=lista_funcoes[indice], width=25, relief='groove', overrelief='flat', font=['Verdana','9'])
                botao.pack(side='left')
        else:
            sistema.erro('Senha Incorreta')
            self.encerrar()

    def menu_usuario(self, usuario):
        self.frame1['pady']=10
        self.frame1.pack()
        divisao = Label(self.frame_menu, text='-'*80, fg=verde, font=font_aviso,bg=cinza)
        divisao.pack()
        voltar=Button(self.frame_menu, command=self.encerrar, bg=cinza, relief='flat', overrelief='flat')
        voltar['image']=self.voltar
        voltar.image=self.voltar
        voltar.pack(side='left')
        informe = Label(self.frame_menu, text='O que deseja fazer {}?'.format(usuario.get_nome()),bg=cinza, fg=azul,font=font_aviso)
        informe.pack()
        subframe=Frame(self.frame_menu, pady=10, bg=cinza)
        subframe.pack()
        retirar = Button(subframe, text='Retirar chave', relief='groove', overrelief='flat', command=lambda:(self.retirar_chave(usuario)), font=['verdana','10'], pady=20, padx=20)
        retirar.pack(side='left')
        devolver=Button(subframe, text='Devolver Chave', relief='groove', overrelief='flat',command=lambda:(self.devolver_chave(usuario)), font=['verdana','10'], pady=20, padx=20)
        devolver.pack(side='left')

    def retirar_chave(self, usuario):
        self.frame_acao.pack_forget()
        self.frame_acao=Frame(self.frame_menu, bg=cinza, pady=20)
        self.frame_acao.pack()
        informe=Label(self.frame_acao, bg=cinza, text='Local da chave a ser RETIRADA:', fg=azul, font=['verdana, 15'])
        informe.pack()
        local=Entry(self.frame_acao,width=20,bd=2, relief='groove', font=['verdana','10'])
        local.pack(side='left')
        botao = Button(self.frame_acao, command=lambda:(sistema.retirar_chave(local.get().upper(), usuario)), relief='flat', overrelief='flat', bg=cinza)
        botao['image'] = self.ir
        botao.image = self.ir
        botao.pack(side='left')


    def devolver_chave(self, usuario):
        self.frame_acao.pack_forget()
        self.frame_acao = Frame(self.frame_menu, bg=cinza, pady=20)
        self.frame_acao.pack()
        informe = Label(self.frame_acao, bg=cinza, text='Local da chave a ser DEVOLVIDA:', fg=azul, font=['verdana, 15'])
        informe.pack()
        local = Entry(self.frame_acao, width=20, bd=2, relief='groove', font=['verdana', '10'])
        local.pack(side='left')
        botao = Button(self.frame_acao, command=lambda: (sistema.devolver_chave(local.get().upper(), usuario)),relief='flat', overrelief='flat', bg=cinza)
        botao['image'] = self.ir
        botao.image = self.ir
        botao.pack(side='left')

    def cadastrar_usuario(self):
        self.frame_acao.pack_forget()
        self.frame_acao = Frame(self.frame_menu, bg=cinza, pady=10)
        self.frame_acao.pack()
        informe=Label(self.frame_acao, text="Cadastrar Usuário", font=font_aviso, fg=cinza_escuro, bg=cinza)
        informe.pack()
        inf_nome=Label(self.frame_acao, text="Nome:", font=font_aviso, fg=cinza_escuro, bg=cinza)
        inf_nome.pack()
        nome=Entry(self.frame_acao, font=['verdana','10'], relief='groove', bd=2, width=50)
        nome.pack()
        inf_matricula=Label(self.frame_acao, text="Matricula:", font=font_aviso, fg=cinza_escuro, bg=cinza)
        inf_matricula.pack()
        matricula=Entry(self.frame_acao, font=['verdana','10'], relief='groove', bd=2, width=25)
        matricula.pack()
        botao=Button(self.frame_acao, relief='flat',bg=cinza, overrelief='flat', command=lambda:sistema.cadastrar_usuario(nome.get().upper(), matricula.get().upper()))
        botao['image']=self.mais
        botao.image=self.mais
        botao.pack()


    def cadastrar_chave(self):
        self.frame_acao.pack_forget()
        self.frame_acao = Frame(self.frame_menu, bg=cinza, pady=20)
        self.frame_acao.pack()
        informe = Label(self.frame_acao, text="Cadastrar Chave", font=font_aviso, fg=cinza_escuro, bg=cinza)
        informe.pack()
        inf_local = Label(self.frame_acao, text="Local no qual a chave se refere:", font=font_aviso, fg=cinza_escuro, bg=cinza)
        inf_local.pack()
        local = Entry(self.frame_acao, font=['verdana', '10'], relief='groove', bd=2, width=25)
        local.pack()
        botao = Button(self.frame_acao, relief='flat', bg=cinza, overrelief='flat',command=lambda: sistema.cadastrar_chave(local.get().upper()))
        botao['image'] = self.mais
        botao.image = self.mais
        botao.pack()

    def cadastrar_memorando(self):
        self.frame_acao.pack_forget()
        self.frame_acao = Frame(self.frame_menu, bg=cinza, pady=20)
        self.frame_acao.pack()
        informe=Label(self.frame_acao, text="Cadastrar Memorando: ", font=font_aviso, bg=cinza, fg=cinza_escuro)
        informe.pack()
        inf_local=Label(self.frame_acao, text="Local no qual os alunos terão acesso:", font=['verdana','12'], bg=cinza, fg=cinza_escuro)
        inf_local.pack()
        ent_local=Entry(self.frame_acao, font=['Verdana', '10'], relief='groove', bd=2, width=25)
        ent_local.pack()
        inf_prof = Label(self.frame_acao, text="Matricula do professor que dará o acesso:", font=['verdana', '12'],bg=cinza, fg=cinza_escuro)
        inf_prof.pack()
        ent_prof = Entry(self.frame_acao, font=['Verdana', '10'], relief='groove', bd=2, width=25)
        ent_prof.pack()
        inf_ence = Label(self.frame_acao, text="Data de encerramento:[DD/MM/AAAA]", font=['verdana', '12'],bg=cinza, fg=cinza_escuro)
        inf_ence.pack()
        ent_ence = Entry(self.frame_acao, font=['Verdana', '10'], relief='groove', bd=2, width=25)
        ent_ence.pack()
        inf_alunos = Label(self.frame_acao, text="Matricula dos alunos separadas por virgula(,)", font=['verdana', '12'], bg=cinza, fg=cinza_escuro)
        inf_alunos.pack()
        ent_alunos = Entry(self.frame_acao, font=['Verdana', '10'], relief='groove', bd=2, width=75)
        ent_alunos.pack()
        mais=Button(self.frame_acao, relief='flat', overrelief='flat', bg=cinza, command=lambda:sistema.cadastrar_memorando(ent_local.get().upper(), ent_prof.get().upper(), ent_alunos.get().upper().split(','), ent_ence.get().upper()))
        mais['image']=self.mais
        mais.image=self.mais
        mais.pack()



    def remover_usuario(self):
        self.frame_acao.pack_forget()
        self.frame_acao = Frame(self.frame_menu, bg=cinza, pady=20)
        self.frame_acao.pack()
        informe = Label(self.frame_acao, text="Remover Usuário", font=font_aviso, fg=vermelho, bg=cinza)
        informe.pack()
        inf_matricula = Label(self.frame_acao, text="Matricula do Usuário:", font=font_aviso, fg=vermelho,bg=cinza)
        inf_matricula.pack()
        matricula = Entry(self.frame_acao, font=['verdana', '10'], relief='groove', bd=2, width=25)
        matricula.pack()
        botao = Button(self.frame_acao, relief='flat', bg=cinza, overrelief='flat',command=lambda: sistema.remover_usuario(matricula.get().upper()))
        botao['image'] = self.excluir
        botao.image = self.excluir
        botao.pack()


    def remover_chave(self):
        self.frame_acao.pack_forget()
        self.frame_acao = Frame(self.frame_menu, bg=cinza, pady=20)
        self.frame_acao.pack()
        informe = Label(self.frame_acao, text="Remover Chave", font=font_aviso, fg=vermelho, bg=cinza)
        informe.pack()
        inf_local = Label(self.frame_acao, text="Local no qual a chave se refere:", font=font_aviso, fg=vermelho,bg=cinza)
        inf_local.pack()
        local = Entry(self.frame_acao, font=['verdana', '10'], relief='groove', bd=2, width=25)
        local.pack()
        botao = Button(self.frame_acao, relief='flat', bg=cinza, overrelief='flat',command=lambda: sistema.remover_chave(local.get().upper()))
        botao['image'] = self.excluir
        botao.image = self.excluir
        botao.pack()

    def alterar_matricula(self):
        self.frame_acao.pack_forget()
        self.frame_acao = Frame(self.frame_menu, bg=cinza, pady=20)
        self.frame_acao.pack()
        informe = Label(self.frame_acao, text="Alterar Matricula de Administrador", font=font_aviso, fg=verde, bg=cinza)
        informe.pack()
        inf_local = Label(self.frame_acao, text="Nova Matricula:", font=font_aviso, fg=verde,bg=cinza)
        inf_local.pack()
        matricula = Entry(self.frame_acao, font=['verdana', '10'], relief='groove', bd=2, width=25)
        matricula.pack()
        botao = Button(self.frame_acao, relief='flat', bg=cinza, overrelief='flat',command=lambda: sistema.alterar_matricula_admin(matricula.get().upper()))
        botao['image'] = self.ir
        botao.image = self.ir
        botao.pack()

    def alterar_senha(self):
        self.frame_acao.pack_forget()
        self.frame_acao = Frame(self.frame_menu, bg=cinza, pady=20)
        self.frame_acao.pack()
        informe = Label(self.frame_acao, text="Alterar Senha de Administrador", font=font_aviso, fg=verde, bg=cinza)
        informe.pack()
        inf_senha1 = Label(self.frame_acao, text="Nova Senha:", font=font_aviso, fg=verde, bg=cinza)
        inf_senha1.pack()
        senha1 = Entry(self.frame_acao, font=['verdana', '10'], relief='groove', bd=2, width=25)
        senha1.pack()
        inf_senha2 = Label(self.frame_acao, text="Confirmar Senha:", font=font_aviso, fg=verde, bg=cinza)
        inf_senha2.pack()
        senha2 = Entry(self.frame_acao, font=['verdana', '10'], relief='groove', bd=2, width=25)
        senha2.pack()
        botao = Button(self.frame_acao, relief='flat', bg=cinza, overrelief='flat',command=lambda: sistema.alterar_senha(senha1.get().upper(), senha2.get().upper()))
        botao['image'] = self.ir
        botao.image = self.ir
        botao.pack()

def rgb(rgb):
    return "#%02x%02x%02x" % rgb

cinza_escuro=rgb((120,120,120))
cinza=rgb((230,230,230))
font_aviso=['verdana','15', 'bold']
verde=rgb((49,175,145))
vermelho=rgb((255,0,0))
azul=rgb((50,50,255))

principal = Tk() #TELA PRINCIPAL
interface=Interface(principal)
sistema=Sistema(interface)
principal['bg']=cinza
principal.geometry('1000x800') #TAMANHO
principal.title('Controle de Chaves') #TITULO
principal.wm_iconbitmap('icone.ico') #ICONE
principal.mainloop() #RODAR TELA PRINCIPAL



