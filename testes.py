import sqlite3
conexao = sqlite3.connect("Controle_de_Chave.db")
cursor=conexao.cursor()

memorandos=[]
memorando=''
for tupla in cursor.execute('select * from Memorando'):
    local=tupla[0]
    professor=tupla[1]
    if memorando == '':
        memorando=list(tupla)
        memorandos.append(memorando)
    elif memorando[0] == local and memorando[1] != professor:
        memorando = list(tupla)
        memorandos.append(memorando)
    elif memorando[0] != local and memorando[1] ==  professor:
        memorando = list(tupla)
        memorandos.append(memorando)

for memorando in memorandos:
    local=memorando[0]
    professor=memorando[1]
    memorando.pop(2)
    memorando.insert(2,[])
    for aluno in cursor.execute('select aluno from Memorando where local=? and professor=?', (local, professor)):
        memorando[2].insert(2,aluno[0])


print(memorandos)










