from sistema import Sistema
from tkinter import *

sistema=Sistema()

principal = Tk()

#tamanho na tela
principal.geometry("800x600")

#titulo
principal.title("Retirar Chaves")
#icone
principal.wm_iconbitmap('icon.ico')

texto=Label(principal, text="Retirar Chaves", font=("Verdana","15"))
texto.pack(side="top")

principal.mainloop()