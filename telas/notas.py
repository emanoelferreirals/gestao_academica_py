from funcs import carregar_dados, salvar_dados, on_close, abrir_nova_tela, acessar_bd, carregar_lista_materias, carregar_periodos
import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox  # Para mostrar a janela de aviso

def exibir_tela(element):
    # Criando os frames
    frame_botoes = tk.Frame(element, padx=10, pady=10)
    frame_botoes.grid(row=0, column=0, padx=20, pady=50, sticky="n")

    frame_principal = tk.Frame(element, padx=20, pady=20)
    frame_principal.grid(row=0, column=1, padx=20, pady=20)

    # Adicionando um título para a tabela
    label_titulo = tk.Label(frame_principal, text="Notas Acadêmicas", font=("Arial", 14, "bold"))
    label_titulo.grid(row=0, column=0, pady=10)

    # Criando um Canvas para a tabela
    canvas_tabela = tk.Canvas(frame_principal, width=900, height=700)
    canvas_tabela.grid(row=1, column=0)

    # Criando a Scrollbar vertical
    scrollbar_tabela = tk.Scrollbar(frame_principal, orient="vertical", command=canvas_tabela.yview)
    scrollbar_tabela.grid(row=1, column=1, sticky="ns")

    # Criando um frame dentro do Canvas para a tabela
    frame_conteudo_tabela = tk.Frame(canvas_tabela)
    canvas_tabela.create_window((0, 0), window=frame_conteudo_tabela, anchor="nw")

    # Configurando o Canvas para funcionar com a Scrollbar
    canvas_tabela.configure(yscrollcommand=scrollbar_tabela.set)

    # Função para calcular a média das notas
    def calcular_media(*notas):
        total = sum(notas)
        return total / len(notas) if len(notas) > 0 else 0

    # Função para excluir uma linha
    def excluir_linha(row_widgets):
        for widget in row_widgets:
            widget.destroy()
        salvar()

    def abrir_cadastro_notas(tela_atual):
        abrir_nova_tela(tela_atual, "cadastro_materias_tela.py", False)

    # Função para adicionar uma linha à tabela
    def adicionar_linha():
        row = len(frame_conteudo_tabela.winfo_children()) // len(titulos) + 1

        cmb_materia = tk.StringVar(value=" ")
        menu_materia = tk.OptionMenu(frame_conteudo_tabela, cmb_materia, *materias)
        menu_materia.config(width=16)
        menu_materia.grid(row=row, column=0, padx=5, pady=5)

        # Obtendo o período da matéria selecionada
        def atualizar_periodo(*args):
            materia = cmb_materia.get()
            if materia:
                dados_materia = acessar_bd("r", f"data/materias/{materia}.json")
                periodo = dados_materia.get("Período", " ")
                lbl_periodo.config(text=periodo)

        cmb_materia.trace("w", atualizar_periodo)

        lbl_periodo = tk.Label(frame_conteudo_tabela, text=" ")
        lbl_periodo.grid(row=row, column=1, padx=5, pady=5)

        entries = []
        for col in range(2, 6):
            entry = tk.Entry(frame_conteudo_tabela, width=5)
            entry.grid(row=row, column=col, padx=5, pady=5)
            entries.append(entry)

        # Calculando a média
        def atualizar_media():
            notas = [int(entry.get() or 0) for entry in entries]
            media = calcular_media(*notas)
            label_media.config(text=f'{media:.2f}')

        for entry in entries:
            entry.bind("<KeyRelease>", lambda event: atualizar_media())

        # Label para exibir a média
        label_media = tk.Label(frame_conteudo_tabela, text="0.00")
        label_media.grid(row=row, column=6, padx=5, pady=5)

        # Botão para excluir a linha
        btn_excluir = tk.Button(frame_conteudo_tabela, text="Excluir", command=lambda r=row: excluir_linha(frame_conteudo_tabela.grid_slaves(row=r)))
        btn_excluir.grid(row=row, column=7, padx=5, pady=5)

        frame_conteudo_tabela.update_idletasks()
        canvas_tabela.configure(scrollregion=canvas_tabela.bbox("all"))

    btn_adicionar_linha = tk.Button(frame_botoes, text="Adicionar Linha", width=20, command=lambda: adicionar_linha())
    btn_adicionar_linha.grid(row=2, column=0, pady=10)

    # Botão para salvar alterações
    btn_salvar = tk.Button(frame_botoes, text="Salvar Alterações", width=20, command=lambda: salvar())
    btn_salvar.grid(row=3, column=0, pady=10)

    # Cabeçalhos da tabela
    titulos = ["Matéria", "Período", "n1", "n2", "n3", "n4", "Média", ""]
    for col, titulo in enumerate(titulos):
        tk.Label(frame_conteudo_tabela, text=titulo, font=("Arial", 10, "bold"), padx=5, pady=5).grid(row=0, column=col)

    # Lista de matérias e períodos disponíveis
    materias = carregar_lista_materias() or [" "]
    semestres = carregar_periodos()

    """------------------------GERENCIAMENTO DA TABELA-----------------------------------"""

    def salvar():
        dados = []  # Lista para armazenar múltiplas linhas

        widgets = frame_conteudo_tabela.winfo_children()

        # Cabeçalhos da tabela
        titulos = ["Matéria", "Período", "n1", "n2", "n3", "n4", "Média", ""]

        # Dicionário temporário para armazenar uma linha completa
        dados_por_linha = {}

        linha_atual = -1  # Variável para rastrear mudanças de linha

        for widget in widgets:
            info = widget.grid_info()
            row = info["row"]
            col = info["column"]

            if col >= len(titulos):
                continue

            coluna_nome = titulos[col]  # Nome da coluna com base no índice

            # Se mudamos de linha, salvamos a anterior e iniciamos uma nova
            if row != linha_atual:
                if dados_por_linha:  # Salva a linha anterior (se houver)
                    dados.append(dados_por_linha)
                dados_por_linha = {}  # Reseta para uma nova linha
                linha_atual = row  # Atualiza a linha atual

            if isinstance(widget, tk.OptionMenu):
                var_name = widget.cget("textvariable")
                valor = widget.getvar(var_name)

            elif isinstance(widget, tk.Entry):
                valor = widget.get().strip()

            elif isinstance(widget, tk.Label):
                valor = widget.cget("text").strip()
            else:
                continue

            # Converter valores numéricos
            if coluna_nome == "Período" or coluna_nome.startswith("n"):
                try:
                    valor = int(valor)
                except ValueError:
                    valor = 0  # Caso esteja vazio ou inválido

            # Adicionar o valor ao dicionário da linha atual
            dados_por_linha[coluna_nome] = valor

        # Salvar a última linha capturada
        if dados_por_linha:
            dados.append(dados_por_linha)

        salvar_dados(dados)
        preencher_tabela()
        Messagebox.ok("Alterações feitas com sucesso!", "Aviso")

    def preencher_tabela():
        dados = carregar_dados()

        # Ordenar os dados pelo valor do período (menor para maior)
        dados_ordenados = sorted(dados, key=lambda x: int(x.get("Período", 0)))

        # Limpar a tabela existente
        for widget in frame_conteudo_tabela.winfo_children():
            widget.destroy()

        # Recriar os cabeçalhos
        for col, titulo in enumerate(titulos):
            tk.Label(frame_conteudo_tabela, text=titulo, font=("Arial", 10, "bold"), padx=5, pady=5).grid(row=0, column=col)

        # Preencher as linhas com os dados carregados e ordenados
        for row, dado in enumerate(dados_ordenados, start=1):
            cmb_materia = tk.StringVar(value=dado.get("Matéria", ""))
            lbl_periodo = tk.Label(frame_conteudo_tabela, text=dado.get("Período", ""))

            menu_materia = tk.OptionMenu(frame_conteudo_tabela, cmb_materia, *materias)
            menu_materia.config(width=16)
            menu_materia.grid(row=row, column=0, padx=5, pady=5)

            lbl_periodo.grid(row=row, column=1, padx=5, pady=5)

            entries = []
            for col, titulo in enumerate(titulos[2:6], start=2):  # Começa a preencher as notas
                entry = tk.Entry(frame_conteudo_tabela, width=5, textvariable=tk.StringVar(value=dado[titulo.lower()]))
                entry.grid(row=row, column=col, padx=5, pady=5)
                entries.append(entry)

            # Calculando a média
            notas = [int(entry.get() or 0) for entry in entries]
            media = calcular_media(*notas)
            label_media = tk.Label(frame_conteudo_tabela, text=f'{media:.2f}')
            label_media.grid(row=row, column=6, padx=5, pady=5)

            # Botão para excluir a linha
            btn_excluir = tk.Button(frame_conteudo_tabela, text="Excluir", command=lambda r=row: excluir_linha(frame_conteudo_tabela.grid_slaves(row=r)))
            btn_excluir.grid(row=row, column=7, padx=5, pady=5)

        frame_conteudo_tabela.update_idletasks()
        canvas_tabela.configure(scrollregion=canvas_tabela.bbox("all"))

    # Adicionando uma linha inicial
    adicionar_linha()

    # Carregar os dados e preencher a tabela ao iniciar a interface
    preencher_tabela()

    # Rodando a interface
    element.mainloop()

# Exemplo de uso
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gerenciamento de Notas")
    root.geometry("1200x800")

    # Inicializando a interface
    exibir_tela(root)