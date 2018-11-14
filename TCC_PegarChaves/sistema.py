from chaveDAO import ChaveDAO

import sqlite3

'''
Este programa tem como objetivo evoluir e, assim, tornar mais segura a forma de pegar chaves em empresas ou escolas/universidades.

This program aims to evolve and thus make safer the way to pick up keys in companies or schools/universities
'''

conexao = sqlite3.connect('TCC_PegarChaves.db')
cursor = conexao.cursor()

chaveDAO = ChaveDAO(conexao, cursor)

class Sistema:

    def __init__(self):
        None







'''
André Lucas Medeiros Martins, Brazilian Computer Technician.

Email:
ande.lucas.medeir@gmail.com
'''

