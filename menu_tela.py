import ttkbootstrap as ttk
from PIL import Image, ImageTk  # Importação do Pillow
from funcs import abrir_nova_tela, on_close
from renderizer.centralizar_janela import centralizar_janela
import telas as tl
from telas import cadastro_materias, notas, cadastro_dados_academicos, relatorio, grafico


# Funções para os botões
def logout(root):
    abrir_nova_tela(root,"login_tela.py",True)
    on_close(root)

def abrir_disciplinas(element):
    esconder_widgets(element)
    botao_voltar.pack(pady=10)  # Exibe o botão "Voltar"
    cadastro_materias.exibir_tela(element)  # Exibe a tela de notas na mesma janela

def abrir_graficos(element):
    esconder_widgets(element)
    botao_voltar.pack(pady=10)  # Exibe o botão "Voltar"
    grafico.exibir_tela(element)  # Exibe a tela de notas na mesma janela

def abrir_cursos(element):
    print("Abrindo Meus Cursos...")

def abrir_notas(element):
    esconder_widgets(element)
    botao_voltar.pack(pady=10)  # Exibe o botão "Voltar"
    notas.exibir_tela(element)  # Exibe a tela de notas na mesma janela

def abrir_desempenho(element):
    esconder_widgets(element)
    botao_voltar.pack(pady=10)  # Exibe o botão "Voltar"
    relatorio.exibir_tela(element)  # Exibe a tela de notas na mesma janela

def abrir_conta(element):
    esconder_widgets(element)
    botao_voltar.pack(pady=10)  # Exibe o botão "Voltar"
    cadastro_dados_academicos.exibir_tela(element)  # Exibe a tela de notas na mesma janela

def voltar_para_menu():
    esconder_widgets(canvas)
    exibir_menu(canvas)
    botao_voltar.pack_forget()  # Esconde o botão "Voltar"

def esconder_widgets(root):
    for widget in root.winfo_children():
        widget.pack_forget()
        widget.grid_forget()

def exibir_menu(frame_pai):
    frame_topo = ttk.Frame(frame_pai, bootstyle="light")
    frame_topo.pack(fill='x')

    lbl_usuario = ttk.Label(frame_topo, text="Aluno Carlos", font=("Arial", 12, "bold"), bootstyle="black")
    lbl_usuario.pack(side="left", padx=20, pady=5)

    icon_config = Image.open("resources/icones/logout.png").resize((30, 30))
    icon_config = ImageTk.PhotoImage(icon_config)

    btn_config = ttk.Button(frame_topo, image=icon_config, bootstyle="light", command=lambda: logout(root))
    btn_config.image = icon_config
    btn_config.pack(side="right", padx=10)

    lbl_acesso_rapido = ttk.Label(frame_pai, text="Acesso Rápido", font=("Arial", 12, "bold"), background="#302c9b")
    lbl_acesso_rapido.pack(pady=10)

    frame_botoes = ttk.Frame(frame_pai, bootstyle="light")
    frame_botoes.pack()

    botoes = [
        ("Minhas Disciplinas", "resources/icones/disciplinas.png", abrir_disciplinas),
        ("Gráficos", "resources/icones/graficos.png", abrir_graficos),
        ("Meus Cursos", "resources/icones/cursos.png", abrir_cursos),
        ("Notas", "resources/icones/notas.png", abrir_notas),
        ("Desempenho", "resources/icones/desempenho.png", abrir_desempenho),
        ("Conta", "resources/icones/conta.png", abrir_conta)
    ]

    frame_pai.imagens = []

    for i, (titulo, img_path, funcao) in enumerate(botoes):
        img = Image.open(img_path).resize((150, 150), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        frame_pai.imagens.append(img)

        btn = ttk.Button(frame_botoes, text=titulo, image=img, compound="top", bootstyle="secondary", command=lambda f=funcao: f(frame_pai))
        btn.grid(row=i//3, column=i%3, padx=20, pady=10)

# Definições de tamanho da janela
largura_janela = 1800
altura_janela = 980

# Criando Janela
root = ttk.Window(themename="flatly")
root.title("Menu com Imagens")
centralizar_janela(root, largura_janela, altura_janela)
root.configure(bg="#302c9b")

# Criando um Canvas dentro da janela
canvas = ttk.Canvas(root, width=largura_janela, height=altura_janela, bg="#302c9b", highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Criando o botão "Voltar"
botao_voltar = ttk.Button(root, text="Voltar", bootstyle="danger", command=voltar_para_menu)

exibir_menu(canvas)

root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))

root.mainloop()
