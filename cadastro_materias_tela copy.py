import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tb
from funcs import salvar_materia

def cadastrar_materia():
    nome = entry_nome.get()
    descricao = entry_descricao.get()
    periodo = entry_periodo.get()
    carga_horaria = entry_carga_horaria.get()
    qtd_aulas = entry_qtd_aulas.get()
    duracao_aulas_min = entry_duracao.get()
    horario_aula = []
    conteudos = entry_conteudos.get().split(",")
    
    if not nome or not periodo:
        messagebox.showerror("Erro", "Preencha os campos obrigatórios!")
        return
    
    salvar_materia(nome, descricao, periodo, int(carga_horaria), conteudos, int(qtd_aulas), int(duracao_aulas_min), horario_aula)
    messagebox.showinfo("Sucesso", "Matéria cadastrada com sucesso!")
    root.destroy()

root = tb.Window(themename="superhero")
root.title("Cadastro de Matéria")
root.geometry("1000x400")

frame = tb.Frame(root, padding=10)
frame.pack(pady=10)

tb.Label(frame, text="Nome:").grid(row=0, column=0, sticky="w")
entry_nome = tb.Entry(frame)
entry_nome.grid(row=0, column=1)

tb.Label(frame, text="Descrição:").grid(row=1, column=0, sticky="w")
entry_descricao = tb.Entry(frame)
entry_descricao.grid(row=1, column=1)

tb.Label(frame, text="Período:").grid(row=2, column=0, sticky="w")
entry_periodo = tb.Entry(frame)
entry_periodo.grid(row=2, column=1)

tb.Label(frame, text="Carga Horária:").grid(row=3, column=0, sticky="w")
entry_carga_horaria = tb.Entry(frame)
entry_carga_horaria.grid(row=3, column=1)

tb.Label(frame, text="Qtd Aulas:").grid(row=4, column=0, sticky="w")
entry_qtd_aulas = tb.Entry(frame)
entry_qtd_aulas.grid(row=4, column=1)

tb.Label(frame, text="Duração Aula (min):").grid(row=5, column=0, sticky="w")
entry_duracao = tb.Entry(frame)
entry_duracao.grid(row=5, column=1)

tb.Label(frame, text="Conteúdos (separados por vírgula):").grid(row=6, column=0, sticky="w")
entry_conteudos = tb.Entry(frame)
entry_conteudos.grid(row=6, column=1)

btn_salvar = tb.Button(frame, text="Salvar Matéria", command=cadastrar_materia)
btn_salvar.grid(row=7, column=0, columnspan=2, pady=10)

root.mainloop()
