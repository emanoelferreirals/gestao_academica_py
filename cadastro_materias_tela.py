import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tb
from funcs import salvar_materia, acessar_bd, ler_login
import os

USUARIO = ler_login()["email"]
DATA_PATH = "data/alunos/"

# Variáveis globais
horario_aula_rows = []  # Armazena os horários cadastrados
materias_registradas = []  # Armazena as matérias existentes

def limpar_campos():
    """ Limpa todos os campos do formulário e a tabela de horários. """
    # Limpar os campos de entrada
    entry_nome.delete(0, tk.END)
    entry_descricao.delete(0, tk.END)
    entry_periodo.delete(0, tk.END)
    entry_carga_horaria.delete(0, tk.END)
    entry_qtd_aulas.delete(0, tk.END)
    entry_duracao.delete(0, tk.END)
    entry_conteudos.delete(0, tk.END)

    # Desbloquear e limpar o campo de ID
    entry_id.config(state="normal")
    entry_id.delete(0, tk.END)
    entry_id.config(state="disabled")

    # Limpar tabela de horários
    limpar_tabela_horarios()


def adicionar_linha(frame, pre_dia=None, pre_hr_entrada="", pre_hr_saida=""):
    """ Adiciona uma nova linha na tabela de horários de aula. """
    row_index = len(horario_aula_rows) + 1
    dias_semana = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"]
    if pre_dia is None:
        pre_dia = dias_semana[0]
    dia_var = tk.StringVar(value=pre_dia)
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
    """ Remove todas as linhas da tabela de horários. """
    for widget in frame_horarios.winfo_children():
        widget.destroy()
    horario_aula_rows.clear()

def excluir_materia():
    """ Exclui a matéria selecionada do banco de dados. """
    selecionado = var_materia_selecionada.get()
    id_materia = materias_opcoes.get(selecionado)  
    
    if id_materia is None:
        messagebox.showerror("Erro", "Selecione uma matéria válida para excluir!")
        return
    
    resposta = messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir a matéria '{selecionado}'?")
    if not resposta:
        return

    dados = acessar_bd("r", f"{DATA_PATH}{USUARIO}/notas.json")
    if isinstance(dados, dict) and "dados_academicos" in dados:
        if id_materia in dados["dados_academicos"]["materias"]:
            del dados["dados_academicos"]["materias"][id_materia]
            acessar_bd("w", f"{DATA_PATH}{USUARIO}/notas.json", dados)
            messagebox.showinfo("Sucesso", "Matéria excluída com sucesso!")
            
            # Atualiza lista, limpa campos e redefine tabela
            carregar_materias_registradas()
            atualizar_lista_materias()
            limpar_campos()
        else:
            messagebox.showerror("Erro", "Matéria não encontrada!")
    else:
        messagebox.showerror("Erro", "Erro ao acessar o banco de dados!")


def carregar_materias_registradas():
    """ Carrega a lista de matérias cadastradas. """
    global materias_registradas
    
    dados = acessar_bd("r", f"{DATA_PATH}{USUARIO}/notas.json")
    if isinstance(dados, dict):
        materias_registradas = dados.get("dados_academicos", {}).get("materias", {})
    else:
        materias_registradas = {}

    print("materias_registradas: ",materias_registradas)

    opcoes = ["Cadastrar nova matéria"]
    for id_materia, dados_materia in materias_registradas.items():
        opcoes.append(dados_materia["nome"])  # Agora adiciona o nome da matéria corretamente
        print("Opções: ",opcoes)
    return opcoes

def atualizar_lista_materias():
    """ Atualiza as opções do OptionMenu garantindo que cada matéria tenha um identificador único. """
    global materias_opcoes  # Dicionário para mapear nomes ao ID real
    materias_opcoes = {"Cadastrar nova matéria": None}
    
    for id_materia, dados in materias_registradas.items():
        nome_exibido = f"{dados['nome']} ({id_materia})"
        materias_opcoes[nome_exibido] = id_materia
    
    opcoes_materias = list(materias_opcoes.keys())
    
    # Atualizar o OptionMenu
    menu_materias["menu"].delete(0, "end")  # Limpar menu antigo
    
    for opcao in opcoes_materias:
        menu_materias["menu"].add_command(label=opcao, command=tk._setit(var_materia_selecionada, opcao, atualizar_campos_materia))
    
    var_materia_selecionada.set(opcoes_materias[0])  # Resetar para a primeira opção

def atualizar_campos_materia(*args):
    """ Atualiza os campos ao selecionar uma matéria pelo OptionMenu."""
    selecionado = var_materia_selecionada.get()
    id_materia = materias_opcoes.get(selecionado)

    if id_materia is None:  # "Cadastrar nova matéria"
        btn_excluir.grid_remove()  # Esconde o botão
        
        # Limpa os campos
        entry_id.config(state="normal")
        entry_id.delete(0, tk.END)
        entry_id.config(state="disabled")

        entry_nome.delete(0, tk.END)
        entry_descricao.delete(0, tk.END)
        entry_periodo.delete(0, tk.END)
        entry_carga_horaria.delete(0, tk.END)
        entry_qtd_aulas.delete(0, tk.END)
        entry_duracao.delete(0, tk.END)
        entry_conteudos.delete(0, tk.END)
        limpar_tabela_horarios()
    else:
        btn_excluir.grid()  # Mostra o botão de excluir
        
        materia = materias_registradas[id_materia]

        entry_id.config(state="normal")
        entry_id.delete(0, tk.END)
        entry_id.insert(0, str(id_materia))  # Definindo ID real
        entry_id.config(state="disabled")

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

        limpar_tabela_horarios()
        for horario in materia.get("horario_aula", []):
            adicionar_linha(frame_horarios, pre_dia=horario.get("dia"), pre_hr_entrada=horario.get("hr_entrada"), pre_hr_saida=horario.get("hr_saida"))

def cadastrar_materia():
    """ Salva a matéria no banco de dados. """
    nome = entry_nome.get()
    descricao = entry_descricao.get()
    periodo = entry_periodo.get()
    carga_horaria = entry_carga_horaria.get()
    qtd_aulas = entry_qtd_aulas.get()
    duracao_aulas_min = entry_duracao.get()
    conteudos = entry_conteudos.get().split(",")
    materia_id = entry_id.get()

    if not nome or not periodo:
        messagebox.showerror("Erro", "Preencha os campos obrigatórios: Nome e Período!")
        return

    horario_aula = []
    for row in horario_aula_rows:
        dia = row["dia"].get()
        hr_inicio = row["hr_entrada"].get()
        hr_fim = row["hr_saida"].get()
        if dia and hr_inicio and hr_fim:
            horario_aula.append({"dia": dia, "hr_entrada": hr_inicio, "hr_saida": hr_fim})

    entry_id.config(state="normal")
    materia_id = entry_id.get()
    entry_id.config(state="disabled")

    try:
        salvar_materia(nome, descricao, periodo, int(carga_horaria), conteudos, int(qtd_aulas), int(duracao_aulas_min), horario_aula, materia_id)
        
        # Atualiza a lista de matérias registradas
        carregar_materias_registradas()
        
        # Atualiza o OptionMenu com as novas matérias
        atualizar_lista_materias()
        
        # Limpa os campos após o cadastro
        limpar_campos()
        
        messagebox.showinfo("Sucesso", "Matéria cadastrada com sucesso!")
        
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar matéria: {e}")

root = tb.Window(themename="superhero")
root.title("Cadastro de Matéria")
root.geometry("1000x600")

frame_selecao = tb.Frame(root, padding=10)
frame_selecao.pack(pady=10)

opcoes_materias = carregar_materias_registradas()
# Criar OptionMenu corretamente
var_materia_selecionada = tk.StringVar()
var_materia_selecionada.set("Cadastrar nova matéria")  # Padrão
menu_materias = tk.OptionMenu(root, var_materia_selecionada, "Cadastrar nova matéria")
menu_materias.pack()
# Atualizar a lista ao iniciar
atualizar_lista_materias()

frame = tb.Frame(root, padding=10)
frame.pack(pady=10)

# Criando labels e campos de entrada
tb.Label(frame, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_nome = tb.Entry(frame, width=40)
entry_nome.grid(row=0, column=1, padx=5, pady=5)

tb.Label(frame, text="Descrição:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_descricao = tb.Entry(frame, width=40)
entry_descricao.grid(row=1, column=1, padx=5, pady=5)

tb.Label(frame, text="Período:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_periodo = tb.Entry(frame, width=40)
entry_periodo.grid(row=2, column=1, padx=5, pady=5)

tb.Label(frame, text="Carga Horária:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
entry_carga_horaria = tb.Entry(frame, width=40)
entry_carga_horaria.grid(row=3, column=1, padx=5, pady=5)

tb.Label(frame, text="Qtd Aulas:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
entry_qtd_aulas = tb.Entry(frame, width=40)
entry_qtd_aulas.grid(row=4, column=1, padx=5, pady=5)

tb.Label(frame, text="Duração Aulas (min):").grid(row=5, column=0, padx=5, pady=5, sticky="w")
entry_duracao = tb.Entry(frame, width=40)
entry_duracao.grid(row=5, column=1, padx=5, pady=5)

tb.Label(frame, text="Conteúdos:").grid(row=6, column=0, padx=5, pady=5, sticky="w")
entry_conteudos = tb.Entry(frame, width=40)
entry_conteudos.grid(row=6, column=1, padx=5, pady=5)

# Criando o campo entry_id invisível
entry_id = tb.Entry(root)
entry_id.config(state="disabled")
entry_id.pack_forget()

frame_horarios = tb.Frame(frame, padding=5)
frame_horarios.grid(row=8, column=0, columnspan=2)

btn_add_horario = tb.Button(frame, text="Adicionar Horário", command=lambda: adicionar_linha(frame_horarios))
btn_add_horario.grid(row=9, column=0, columnspan=2, pady=10)

btn_salvar = tb.Button(frame, text="Salvar Matéria", command=cadastrar_materia)
btn_salvar.grid(row=10, column=0, columnspan=2, pady=10)

btn_excluir = tb.Button(frame, text="Excluir Matéria", command=excluir_materia)
btn_excluir.grid(row=11, column=0, columnspan=2, pady=10)
btn_excluir.grid_remove()  # Esconde o botão por padrão

root.mainloop()
