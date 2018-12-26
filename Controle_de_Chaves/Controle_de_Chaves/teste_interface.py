from tkinter import *
from sistema_adaptado import *

class Interface:

    def __init__(self,  container):
        self.principal=container
        self.tela_principal()

    def tela_principal(self):
        self.frame1 = Frame(self.principal, pady=120)
        self.frame2 = Frame(self.principal, pady=5)
        self.frame_menu = Frame(self.principal, pady=20)
        self.frame_aviso=Frame(self.principal, pady=5)

        self.frame1.pack()
        self.frame2.pack()
        self.frame_menu.pack()
        self.frame_aviso.pack(side='bottom')

        self.frame_menu['bg'] = cinza
        self.frame1['bg'] = cinza
        self.frame2['bg'] = cinza
        self.frame_aviso['bg'] = cinza


        self.erro=Label(self.frame_aviso, font=font_aviso, fg=vermelho, bg=cinza)
        self.aviso=Label(self.frame_aviso, font=font_aviso, fg=verde, bg=cinza)

        self.ir = PhotoImage(file='feito.ppm')
        self.voltar=PhotoImage(file='voltar.ppm')

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
            opcao=''
            while opcao != 'X':
                self.matricula.delete(0, END)
                opcao=self.menu_administrador()
        else:
            usuario = sistema.buscar_usuario(self.matricula.get().upper())
            if usuario != None:
                self.matricula.delete(0, END)
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
        self.frame_aviso.pack_forget()

    def encerrar(self):
        self.limpar_tela()
        self.tela_principal()


    def menu_administrador(self):
        self.frame1['pady'] = 10
        self.frame1.pack()
        print('x')
        return 'X'

    def menu_usuario(self, usuario):
        self.frame1['pady']=10
        self.frame1.pack()
        divisao = Label(self.frame_menu, text='-'*80, fg=verde, font=font_aviso,bg=cinza)
        divisao.pack()

        voltar=Button(self.frame_menu, command=self.encerrar, bg=cinza, relief='flat', overrelief='flat')
        voltar['image']=self.voltar
        voltar.image=self.voltar
        voltar.pack(side='left')

        informe = Label(self.frame_menu, text='O que deseja fazer {}?'.format(usuario.get_nome()),bg=cinza, fg=azul,font=['verdana', '10', 'bold'])
        informe.pack()

        subframe=Frame(self.frame_menu, pady=20, bg=cinza)
        subframe.pack()
        retirar = Button(subframe, text='Retirar chave', relief='groove', overrelief='flat', command=lambda:(self.retirar_chave(usuario)), font=['verdana','10'], pady=20, padx=20)
        retirar.pack(side='left')
        devolver=Button(subframe, text='Devolver Chave', relief='groove', overrelief='flat',command=lambda:(self.devolver_chave(usuario)), font=['verdana','10'], pady=20, padx=20)
        devolver.pack(side='left')

    def retirar_chave(self, usuario):
        frame_acao=Frame(self.frame_menu, bg=cinza, pady=20)
        frame_acao.pack()
        informe=Label(frame_acao, bg=cinza, text='Local da chave a ser RETIRADA:', fg=azul, font=['verdana, 15'])
        informe.pack()
        local=Entry(frame_acao,width=20,bd=2, relief='groove', font=['verdana','10'])
        local.pack(side='left')
        lancar = Button(frame_acao, command=lambda:(sistema.retirar_chave(local.get().upper(), usuario)), relief='flat', overrelief='flat', bg=cinza)
        lancar['image'] = self.ir
        lancar.image = self.ir
        lancar.pack(side='left')


    def devolver_chave(self, usuario):
        frame_acao = Frame(self.frame_menu, bg=cinza, pady=20)
        frame_acao.pack()
        informe = Label(frame_acao, bg=cinza, text='Local da chave a ser DEVOLVIDA:', fg=azul, font=['verdana, 15'])
        informe.pack()
        local = Entry(frame_acao, width=20, bd=2, relief='groove', font=['verdana', '10'])
        local.pack(side='left')
        lancar = Button(frame_acao, command=lambda: (sistema.devolver_chave(local.get().upper(), usuario)),relief='flat', overrelief='flat', bg=cinza)
        lancar['image'] = self.ir
        lancar.image = self.ir
        lancar.pack(side='left')



def rgb(rgb):
    return "#%02x%02x%02x" % rgb

cinza_escuro=rgb((200,200,200))
cinza=rgb((230,230,230))
font_aviso=['verdana','15', 'bold']
verde=rgb((49,175,145))
vermelho=rgb((255,0,0))
azul=rgb((50,50,255))

principal = Tk() #TELA PRINCIPAL
interface=Interface(principal)
sistema=Sistema(interface)
principal['bg']=cinza
principal.geometry('800x600') #TAMANHO
principal.title('Controle de Chaves') #TITULO
principal.wm_iconbitmap('icone.ico') #ICONE
principal.mainloop() #RODAR TELA PRINCIPAL



