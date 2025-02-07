import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tb
from funcs import salvar_materia  # Certifique-se de que esta função está implementada

# Lista global para armazenar os widgets de cada linha de horário
horario_aula_rows = []

def adicionar_linha(frame):
    """Adiciona uma nova linha na tabela de horários de aula."""
    # Linha 0 é o cabeçalho; a nova linha será indexada conforme o tamanho da lista + 1
    row_index = len(horario_aula_rows) + 1
    # Lista de dias da semana
    dias_semana = ["segunda-feira", "terça-feira", "quarta-feira", 
                   "quinta-feira", "sexta-feira", "sábado", "domingo"]
    
    # Variável para o dia, com valor padrão
    dia_var = tk.StringVar(value=dias_semana[0])
    # Cria o OptionMenu passando os dias como argumentos posicionais
    om_dia = tb.OptionMenu(frame, dia_var, *dias_semana)
    om_dia.grid(row=row_index, column=0, padx=5, pady=2)
    
    # Campo para horário de entrada
    entry_inicio = tb.Entry(frame, width=10)
    entry_inicio.grid(row=row_index, column=1, padx=5, pady=2)
    
    # Campo para horário de saída
    entry_fim = tb.Entry(frame, width=10)
    entry_fim.grid(row=row_index, column=2, padx=5, pady=2)
    
    # Armazena os widgets da linha para posterior leitura
    horario_aula_rows.append({
        "dia": dia_var,
        "hr_entrada": entry_inicio,
        "hr_saida": entry_fim
    })

def cadastrar_materia():
    """Coleta os dados da tela e salva a disciplina, incluindo os horários de aula."""
    nome = entry_nome.get()
    descricao = entry_descricao.get()
    periodo = entry_periodo.get()
    carga_horaria = entry_carga_horaria.get()
    qtd_aulas = entry_qtd_aulas.get()
    duracao_aulas_min = entry_duracao.get()
    conteudos = entry_conteudos.get().split(",")
    
    # Validação dos campos obrigatórios
    if not nome or not periodo:
        messagebox.showerror("Erro", "Preencha os campos obrigatórios: Nome e Período!")
        return
    
    # Monta a lista de horários a partir das linhas adicionadas
    horario_aula = []
    for row in horario_aula_rows:
        dia = row["dia"].get()
        hr_inicio = row["hr_entrada"].get()
        hr_fim = row["hr_saida"].get()
        # Inclui a linha se todos os campos estiverem preenchidos
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
root.geometry("1000x500")

# Frame principal para os campos da disciplina
frame = tb.Frame(root, padding=10)
frame.pack(pady=10)

# Campos padrão para cadastro da disciplina
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

# Botão para adicionar uma nova linha de horário
btn_add_horario = tb.Button(frame, text="Adicionar Horário", command=lambda: adicionar_linha(frame_horarios))
btn_add_horario.grid(row=9, column=0, columnspan=2, pady=10)

# Botão para salvar a matéria
btn_salvar = tb.Button(frame, text="Salvar Matéria", command=cadastrar_materia)
btn_salvar.grid(row=10, column=0, columnspan=2, pady=10)

root.mainloop()
