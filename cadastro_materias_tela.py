import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tb
from funcs import salvar_materia, acessar_bd, ler_login
import os

USUARIO = ler_login()["email"]
DATA_PATH = "data/alunos/"

# Variável global para armazenar os horários (cada linha da tabela)
horario_aula_rows = []

# Variável global para armazenar as matérias cadastradas
materias_registradas = []

def adicionar_linha(frame, pre_dia=None, pre_hr_entrada="", pre_hr_saida=""):
    """
    Adiciona uma nova linha na tabela de horários de aula.
    Permite opcionalmente pré-preencher os valores.
    """
    row_index = len(horario_aula_rows) + 1
    dias_semana = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"]
    if pre_dia is None:
        pre_dia = dias_semana[0]
    dia_var = tk.StringVar(value=pre_dia)
    # Corrigindo a criação do OptionMenu: passar os dias com *dias_semana
    om_dia = tb.OptionMenu(frame, dia_var, *dias_semana)
    om_dia.grid(row=row_index, column=0, padx=5, pady=2)
    
    entry_inicio = tb.Entry(frame, width=10)
    entry_inicio.insert(0, pre_hr_entrada)
    entry_inicio.grid(row=row_index, column=1, padx=5, pady=2)
    
    entry_fim = tb.Entry(frame, width=10)
    entry_fim.insert(0, pre_hr_saida)
    entry_fim.grid(row=row_index, column=2, padx=5, pady=2)
    
    horario_aula_rows.append({
        "dia": dia_var,
        "hr_entrada": entry_inicio,
        "hr_saida": entry_fim
    })

def limpar_tabela_horarios():
    """Remove todas as linhas da tabela de horários."""
    for widget in frame_horarios.winfo_children():
        widget.destroy()
    horario_aula_rows.clear()

def carregar_materias_registradas():
    """
    Carrega a lista de matérias cadastradas a partir do JSON.
    Pressupõe que os dados estejam armazenados em:
       dados_academicos -> materias (lista de dicionários)
    """
    global materias_registradas
    
    dados = acessar_bd("r",f"{DATA_PATH}{USUARIO}/notas.json")
    # Tenta acessar as matérias na estrutura: dados_academicos -> materias
    if isinstance(dados, dict):
        materias_registradas = dados.get("dados_academicos", {}).get("materias", [])
    elif isinstance(dados, list):
        materias_registradas = dados
    else:
        materias_registradas = []
    # Retorna uma lista de nomes, com a opção de cadastrar nova matéria no início
    opcoes = ["Cadastrar nova matéria"]
    for materia in materias_registradas:
        nome = materia.get("nome")
        if nome:
            opcoes.append(nome)
    return opcoes

def atualizar_campos_materia(*args):
    """
    Callback chamado quando a seleção do OptionMenu muda.
    Se for "Cadastrar nova matéria", limpa os campos.
    Caso contrário, preenche os campos com os dados da matéria selecionada.
    """
    selecionado = var_materia_selecionada.get()
    if selecionado == "Cadastrar nova matéria":
        # Limpa os campos de cadastro
        entry_nome.delete(0, tk.END)
        entry_descricao.delete(0, tk.END)
        entry_periodo.delete(0, tk.END)
        entry_carga_horaria.delete(0, tk.END)
        entry_qtd_aulas.delete(0, tk.END)
        entry_duracao.delete(0, tk.END)
        entry_conteudos.delete(0, tk.END)
        limpar_tabela_horarios()
    else:
        # Procura a matéria selecionada na lista carregada
        materia = None
        for m in materias_registradas:
            if m.get("nome") == selecionado:
                materia = m
                break
        if materia:
            # Preenche os campos
            entry_nome.delete(0, tk.END)
            entry_nome.insert(0, materia.get("nome", ""))
            entry_descricao.delete(0, tk.END)
            entry_descricao.insert(0, materia.get("descricao", ""))
            entry_periodo.delete(0, tk.END)
            entry_periodo.insert(0, materia.get("periodo", ""))
            entry_carga_horaria.delete(0, tk.END)
            entry_carga_horaria.insert(0, str(materia.get("carga_horaria", "")))
            entry_qtd_aulas.delete(0, tk.END)
            entry_qtd_aulas.insert(0, str(materia.get("qtd_aulas", "")))
            entry_duracao.delete(0, tk.END)
            entry_duracao.insert(0, str(materia.get("duracao_aulas_min", "")))
            entry_conteudos.delete(0, tk.END)
            entry_conteudos.insert(0, ",".join(materia.get("conteudos", [])))
            # Preenche a tabela de horários
            limpar_tabela_horarios()
            for horario in materia.get("horario_aula", []):
                adicionar_linha(frame_horarios,
                    pre_dia=horario.get("dia"),
                    pre_hr_entrada=horario.get("hr_entrada"),
                    pre_hr_saida=horario.get("hr_saida"))

def cadastrar_materia():
    """Coleta os dados da tela e salva a disciplina, incluindo os horários de aula."""
    nome = entry_nome.get()
    descricao = entry_descricao.get()
    periodo = entry_periodo.get()
    carga_horaria = entry_carga_horaria.get()
    qtd_aulas = entry_qtd_aulas.get()
    duracao_aulas_min = entry_duracao.get()
    conteudos = entry_conteudos.get().split(",")
    
    if not nome or not periodo:
        messagebox.showerror("Erro", "Preencha os campos obrigatórios: Nome e Período!")
        return
    
    # Monta a lista de horários a partir das linhas adicionadas
    horario_aula = []
    for row in horario_aula_rows:
        dia = row["dia"].get()
        hr_inicio = row["hr_entrada"].get()
        hr_fim = row["hr_saida"].get()
        if dia and hr_inicio and hr_fim:
            horario_aula.append({
                "dia": dia,
                "hr_entrada": hr_inicio,
                "hr_saida": hr_fim
            })
    
    try:
        salvar_materia(
            nome, 
            descricao, 
            periodo, 
            int(carga_horaria), 
            conteudos, 
            int(qtd_aulas), 
            int(duracao_aulas_min), 
            horario_aula
        )
        messagebox.showinfo("Sucesso", "Matéria cadastrada com sucesso!")
        root.destroy()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar matéria: {e}")

# Criação da janela principal com ttkbootstrap
root = tb.Window(themename="superhero")
root.title("Cadastro de Matéria")
root.geometry("1000x600")

# Frame para o OptionMenu de seleção de matéria
frame_selecao = tb.Frame(root, padding=10)
frame_selecao.pack(pady=10)

# Carrega as matérias já cadastradas e monta a lista de opções
opcoes_materias = carregar_materias_registradas()
print(opcoes_materias)
var_materia_selecionada = tk.StringVar(value=opcoes_materias[0])
optionmenu_materia = tk.OptionMenu(frame_selecao, var_materia_selecionada, *opcoes_materias)
optionmenu_materia.config(width=30)
optionmenu_materia.pack()

# Vincula a mudança de seleção ao callback
var_materia_selecionada.trace("w", atualizar_campos_materia)

# Frame principal para os campos da disciplina
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

# Título para a tabela de horários
tb.Label(frame, text="Horários de Aula:", font=("Arial", 10, "bold")).grid(row=7, column=0, columnspan=2, pady=(20, 5))

# Frame para a tabela de horários
frame_horarios = tb.Frame(frame, padding=5)
frame_horarios.grid(row=8, column=0, columnspan=2)

# Cabeçalho da tabela de horários
tb.Label(frame_horarios, text="Dia").grid(row=0, column=0, padx=5)
tb.Label(frame_horarios, text="Hora de Entrada").grid(row=0, column=1, padx=5)
tb.Label(frame_horarios, text="Hora de Saída").grid(row=0, column=2, padx=5)

# Botão para adicionar nova linha de horário
btn_add_horario = tb.Button(frame, text="Adicionar Horário", command=lambda: adicionar_linha(frame_horarios))
btn_add_horario.grid(row=9, column=0, columnspan=2, pady=10)

# Botão para salvar a matéria
btn_salvar = tb.Button(frame, text="Salvar Matéria", command=cadastrar_materia)
btn_salvar.grid(row=10, column=0, columnspan=2, pady=10)

root.mainloop()
