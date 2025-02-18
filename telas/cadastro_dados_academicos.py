import json
import os
import ttkbootstrap as tb
from funcs import salvar_dados_academicos, acessar_bd, ler_login

def exibir_tela(element_pai):
    # Obtém o usuário logado e o caminho do arquivo JSON
    usuario = ler_login()["email"]
    caminho_arquivo = os.path.join("data/alunos/", usuario, "notas.json")

    # Carrega os dados acadêmicos, se existirem
    banco = acessar_bd("r", caminho_arquivo)
    dados_academicos = banco.get("dados_academicos", {})

    # Criar frame para organizar os elementos
    frame = tb.Frame(element_pai, padding=10)
    frame.pack(fill='both', expand=True)

    # Função auxiliar para criar labels e entries preenchidos
    def criar_campo(label_text, valor_padrao=""):
        tb.Label(frame, text=label_text).pack(anchor='w')
        entry = tb.Entry(frame)
        entry.pack(fill='x')
        entry.insert(0, valor_padrao)  # Preenche com o valor existente, se houver
        return entry

    # Criar os campos preenchidos com os dados existentes
    entry_curso = criar_campo("Curso:", dados_academicos.get("curso", ""))
    entry_instituicao = criar_campo("Instituição:", dados_academicos.get("instituicao", ""))
    entry_qtd_periodos = criar_campo("Quantidade de Períodos:", str(dados_academicos.get("qtd_periodos", "")))
    entry_notas_bimestre = criar_campo("Notas por Bimestre (True/False):", str(dados_academicos.get("notas_bimestre", "False")))
    entry_qtd_notas_periodo = criar_campo("Quantidade de Notas por Período:", str(dados_academicos.get("qtd_notas_periodo", "")))
    entry_carga_horaria = criar_campo("Carga Horária Total:", str(dados_academicos.get("carga_horaria", "")))

    # Função para salvar os dados
    def salvar():
        curso = entry_curso.get()
        instituicao = entry_instituicao.get()
        qtd_periodos = int(entry_qtd_periodos.get() or 0)
        notas_bimestre = entry_notas_bimestre.get().lower() == 'true'
        qtd_notas_periodo = int(entry_qtd_notas_periodo.get() or 0)
        carga_horaria = int(entry_carga_horaria.get() or 0)
        
        salvar_dados_academicos(curso, instituicao, qtd_periodos, notas_bimestre, qtd_notas_periodo, carga_horaria)
        tb.Label(frame, text="Dados salvos com sucesso!", foreground="green").pack()

    # Botão de salvar
    tb.Button(frame, text="Salvar", command=salvar).pack(pady=10)

    # Inicia a interface
    element_pai.mainloop()
