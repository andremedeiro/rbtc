import sqlite3
conexao = sqlite3.connect("Controle_de_Chave.db")

class UsuarioDAO:

    def __init__(self):
        self.criar_tabela()

    def criar_tabela(self):
        cursor=conexao.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS Usuario (nome text, matricula text primary key, tipo text)')
        cursor.close()

    def insere_usuario(self, nome, matricula, tipo):
        cursor = conexao.cursor()
        cursor.execute('INSERT INTO Usuario values (?,?,?)', (nome, matricula, tipo))
        conexao.commit()
        cursor.close()

    def remove_usuario(self, matricula):
        cursor = conexao.cursor()
        cursor.execute('DELETE FROM Usuario WHERE matricula = ?', (matricula,))
        conexao.commit()
        cursor.close()

    def listar_usuarios(self):
        cursor = conexao.cursor()
        lista_usuario = []
        for usuario in cursor.execute('SELECT * FROM Usuario'):
            if usuario != None:
                lista_usuario.append(self.retorna_objeto(usuario))
        cursor.close()
        return lista_usuario

    def buscar_usuario(self, matricula):
        cursor = conexao.cursor()
        for tupla in cursor.execute("SELECT * FROM Usuario"):
            if matricula == tupla[1]:
                return self.retorna_objeto(tupla)
        cursor.close()

    def retorna_objeto(self, tupla):
        from usuario import Usuario
        return Usuario(tupla[0], tupla[1], tupla[2])

