import sqlite3
conexao = sqlite3.connect("Controle_de_Chave.db")
cursor=conexao.cursor()
memorandos = []
for memorando in cursor.execute('select * from Memorando'):
    lista_alunos=[]
    memorando_lista=list(memorando)
    lista_alunos.append(memorando_lista[2])
    memorando_lista.pop(2)
    memorando_lista.insert(2, lista_alunos)
    memorandos.append(memorando_lista)
memorandos_feitos=[]
for memorando in memorandos:
    local = memorando[0]
    professor = memorando[1]
    lista_alunos=memorando[2]
    for outro_memorando in memorandos:
        if outro_memorando[0] == local and outro_memorando[1] == professor:
            aluno=outro_memorando[2]
            lista_alunos.append(aluno[0])
            memorandos.remove(outro_memorando)
    memorandos_feitos.append(memorando)
print(memorandos_feitos)

cursor.close()

def mudar_cor(texto, cor):
    return str('\033[' + str(cor) + 'm' + str(texto) + '\033[0;0m')



