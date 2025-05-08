import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import banco

banco.conectar_banco()

cliente_selecionado_id = None  # Para armazenar ID selecionado

def adicionar_cliente():
    nome = entrada_nome.get()
    email = entrada_email.get()
    telefone = entrada_telefone.get()

    if nome == "" or email == "":
        messagebox.showwarning("Campos obrigatórios", "Nome e e-mail são obrigatórios!")
        return

    conexao = sqlite3.connect("clientes.db")
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)", (nome, email, telefone))
    conexao.commit()
    conexao.close()
    limpar_campos()
    carregar_clientes()

def carregar_clientes():
    for linha in tabela_clientes.get_children():
        tabela_clientes.delete(linha)

    conexao = sqlite3.connect("clientes.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM clientes")
    for cliente in cursor.fetchall():
        tabela_clientes.insert("", tk.END, values=cliente)
    conexao.close()

def limpar_campos():
    global cliente_selecionado_id
    entrada_nome.delete(0, tk.END)
    entrada_email.delete(0, tk.END)
    entrada_telefone.delete(0, tk.END)
    cliente_selecionado_id = None

def selecionar_cliente(evento):
    global cliente_selecionado_id
    item = tabela_clientes.selection()
    if item:
        valores = tabela_clientes.item(item, "values")
        cliente_selecionado_id = valores[0]
        entrada_nome.delete(0, tk.END)
        entrada_email.delete(0, tk.END)
        entrada_telefone.delete(0, tk.END)
        entrada_nome.insert(0, valores[1])
        entrada_email.insert(0, valores[2])
        entrada_telefone.insert(0, valores[3])

def editar_cliente():
    global cliente_selecionado_id
    if not cliente_selecionado_id:
        messagebox.showinfo("Selecionar cliente", "Selecione um cliente na tabela para editar.")
        return

    nome = entrada_nome.get()
    email = entrada_email.get()
    telefone = entrada_telefone.get()

    conexao = sqlite3.connect("clientes.db")
    cursor = conexao.cursor()
    cursor.execute("UPDATE clientes SET nome=?, email=?, telefone=? WHERE id=?", (nome, email, telefone, cliente_selecionado_id))
    conexao.commit()
    conexao.close()
    limpar_campos()
    carregar_clientes()

def excluir_cliente():
    global cliente_selecionado_id
    if not cliente_selecionado_id:
        messagebox.showinfo("Selecionar cliente", "Selecione um cliente na tabela para excluir.")
        return

    resposta = messagebox.askyesno("Confirmar exclusão", "Tem certeza que deseja excluir este cliente?")
    if resposta:
        conexao = sqlite3.connect("clientes.db")
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM clientes WHERE id=?", (cliente_selecionado_id,))
        conexao.commit()
        conexao.close()
        limpar_campos()
        carregar_clientes()

# Interface
janela = tk.Tk()
janela.title("Cadastro de Clientes")

tk.Label(janela, text="Nome").grid(row=0, column=0)
entrada_nome = tk.Entry(janela)
entrada_nome.grid(row=0, column=1)

tk.Label(janela, text="E-mail").grid(row=1, column=0)
entrada_email = tk.Entry(janela)
entrada_email.grid(row=1, column=1)

tk.Label(janela, text="Telefone").grid(row=2, column=0)
entrada_telefone = tk.Entry(janela)
entrada_telefone.grid(row=2, column=1)

tk.Button(janela, text="Adicionar Cliente", command=adicionar_cliente).grid(row=3, column=0, columnspan=2, pady=5)
tk.Button(janela, text="Editar Cliente", command=editar_cliente).grid(row=4, column=0, columnspan=2, pady=5)
tk.Button(janela, text="Excluir Cliente", command=excluir_cliente).grid(row=5, column=0, columnspan=2, pady=5)

# Tabela
tabela_clientes = ttk.Treeview(janela, columns=("id", "nome", "email", "telefone"), show="headings")
tabela_clientes.heading("id", text="ID")
tabela_clientes.heading("nome", text="Nome")
tabela_clientes.heading("email", text="E-mail")
tabela_clientes.heading("telefone", text="Telefone")
tabela_clientes.grid(row=6, column=0, columnspan=2, pady=10)
tabela_clientes.bind("<Double-1>", selecionar_cliente)

carregar_clientes()
janela.mainloop()
