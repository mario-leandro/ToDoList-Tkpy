from tkinter import *
from tkinter import messagebox
import mysql.connector

##---------------------------Funções da lista de tarefas---------------------------##
#---------------------------Adicionar tarefa---------------------------#
def adicionar_tarefa():
    descricao = nome_tarefa_input.get()
    data_inicio = data_inicio_input.get()
    data_fim = data_fim_input.get()
    
    if descricao and data_inicio and data_fim:
        sql = "INSERT INTO tarefa(nome_tarefa, data_inicio, data_fim, concluida) VALUES (%s, %s, %s, %s)"
        valores = (descricao, data_inicio, data_fim, False)
        cursor.execute(sql, valores)
        conexao.commit()
        nome_tarefa_input.delete(0, END)
        data_inicio_input.delete(0, END)
        data_fim_input.delete(0, END)
        mostrar_tarefas()

#---------------------------Mostrar tarefa---------------------------#
def mostrar_tarefas():
    mostrar_tarefas_box.delete(0, END)
    sql = "SELECT * FROM tarefa"
    cursor.execute(sql)
    tarefas = cursor.fetchall()
    for tarefa in tarefas:
        descricao = tarefa[1]
        concluido = "Concluído" if tarefa[2] else "Em andamento"
        mostrar_tarefas_box.insert(END, f"{descricao} - {concluido}")

#---------------------------Concluir tarefa---------------------------#
def concluir_tarefa():
    indice_selecionado = mostrar_tarefas_box.curselection()
    if indice_selecionado:
        id_tarefa_selecionada = indice_selecionado[0] + 1
        sql = "UPDATE tarefa SET concluida = True WHERE id_tarefa = %s"
        valores = (id_tarefa_selecionada,)
        cursor.execute(sql, valores)
        conexao.commit()
        mostrar_tarefas()

#---------------------------Deletar tarefa---------------------------#
def deletar_tarefa():
    indice_selecionado = mostrar_tarefas_box.curselection()
    if indice_selecionado:
        indice = indice_selecionado[0]
        tarefa_selecionada = mostrar_tarefas_box.get(indice) 
        descricao_tarefa = tarefa_selecionada.split(" - ")[0]  
        sql = "DELETE FROM tarefa WHERE nome_tarefa = %s"
        valores = (descricao_tarefa,)
        cursor.execute(sql, valores)
        conexao.commit()
        mostrar_tarefas()

#---------------------------Interface---------------------------#
janela = Tk()
janela.geometry("500x600")
janela.title("Lista de tarefas")
janela.configure(background="#000000")
janela.resizable(True, True)
janela.maxsize(width=900, height=700)
janela.minsize(width=300, height=600)

##---------------------------Frame---------------------------##
# Aqui ficará o input e os botões
criar_tarefas_box = Frame(janela, 
bg="#222222",
highlightbackground="#FF0000",
highlightcolor="#FF0000",
highlightthickness=1,)
criar_tarefas_box.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)

#---------------------------Caixa aonde ficará as tarefas---------------------------#
mostrar_tarefas_box = Listbox(janela, 
bg="#222222", 
fg="#FFFFFF", 
selectmode=SINGLE, 
bd="0",
highlightbackground="#FF0000",
highlightcolor="#FF0000",
selectbackground="#FFFFFF",
selectforeground="#000000",
font="Arial, 12")
mostrar_tarefas_box.place(relx=0.02, 
rely=0.51, 
relwidth=0.96, 
relheight=0.46)

#---------------------------Label---------------------------#
nome_tarefa_label = Label(criar_tarefas_box, 
text="Nome tarefa: ", 
bg="#222222", 
fg="#FFFFFF", 
font="Arial, 12", 
pady="10")
nome_tarefa_label.place(relx=0.35, rely=0.001)

data_inicio_label = Label(criar_tarefas_box, 
text="Data de Início:", 
bg="#222222", 
fg="#FFFFFF", 
font="Arial, 12", 
pady="10")
data_inicio_label.place(relx=0.1, rely=0.25)

data_fim_label = Label(criar_tarefas_box, 
text="Data de Fim:", 
bg="#222222", 
fg="#FFFFFF", 
font="Arial, 12", 
pady="10")
data_fim_label.place(relx=0.6, rely=0.25)

#---------------------------Input---------------------------#
nome_tarefa_input = Entry(criar_tarefas_box, 
bg="#222222", 
fg="#FFFFFF",
insertbackground="#FFFFFF",
font="Arial, 10")
nome_tarefa_input.place(relx=0.35, 
rely=0.13, 
relwidth=0.33, 
relheight=0.08)

data_inicio_input = Entry(criar_tarefas_box, 
bg="#222222", 
fg="#FFFFFF", 
insertbackground="#FFFFFF",
font="Arial, 10")
data_inicio_input.place(relx=0.1, 
rely=0.37, 
relwidth=0.33, 
relheight=0.08)

data_fim_input = Entry(criar_tarefas_box, 
bg="#222222", 
fg="#FFFFFF", 
insertbackground="#FFFFFF",
font="Arial, 10")
data_fim_input.place(relx=0.6, 
rely=0.37, 
relwidth=0.33, 
relheight=0.08)

#---------------------------Botões---------------------------#
adicionar_tarefa = Button(criar_tarefas_box, 
text="Adicionar Tarefa", 
border="1px", 
command=adicionar_tarefa)
adicionar_tarefa.place(relx=0.1, 
rely=0.5, 
relwidth=0.33, 
relheight=0.1)


mostrar_tarefa = Button(criar_tarefas_box, 
text="Mostrar Tarefas", 
border="1px", 
command=mostrar_tarefas)
mostrar_tarefa.place(relx=0.1, 
rely=0.63, 
relwidth=0.33, 
relheight=0.1)

concluir_tarefa_button = Button(criar_tarefas_box, 
text="Concluir Tarefa",  
activebackground="#00BB00", 
activeforeground="#FFFFFF", 
border="1px", 
command=concluir_tarefa)
concluir_tarefa_button.place(relx=0.6, 
rely=0.5, 
relwidth=0.33, 
relheight=0.1)

deletar_tarefa_button = Button(criar_tarefas_box, 
text="Deletar Tarefa", 
activebackground="#FF0000",
activeforeground="#FFFFFF",
border="1px", 
command=deletar_tarefa)
deletar_tarefa_button.place(relx=0.6, 
rely=0.63, 
relwidth=0.33, 
relheight=0.1)

#---------------------------Banco de dados---------------------------#
try:
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='projeto_python'
    )

    cursor = conexao.cursor()
except mysql.connector.Error as err:
    messagebox.showerror("Erro de Conexão", f"Ocorreu um erro ao conectar ao banco de dados: {err}")
    janela.quit()

#---------------------------Iniciar Janela Tkinter---------------------------#
mainloop()