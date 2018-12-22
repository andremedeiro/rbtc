from tkinter import *
from sistema import *

class Interface:

    def __init__(self):
        self.principal = Tk() #TELA PRINCIPAL
        self.principal['bg'] = 'light grey'
        self.principal.geometry('800x600') #TAMANHO
        self.principal.title('Controle de Chaves') #TITULO
        self.principal.wm_iconbitmap('chave.ico') #ICONE

        informe=Label(self.principal, text='DIGITE SUA MATRICULA:', font='verdana,15', bg='light grey')
        informe.pack()

        matricula=Entry(self.principal)
        matricula.pack()

        lancar = Button(self.principal, font='verdana, 10')
        lancar.pack()

        aparecer = Label(self.principal, bg='light grey', fg='red')
        aparecer.pack()

        self.principal.mainloop() #RODAR TELA PRINCIPAL

    def reecrever(self, texto):
        return texto

Interface()