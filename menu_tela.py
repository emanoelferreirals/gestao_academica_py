import ttkbootstrap as tb
from PIL import Image, ImageTk  # Importação do Pillow
from funcs import abrir_nova_tela, on_close

# Funções para os botões
def abrir_config(tela_atual):
    print("Abrindo configurações...")

def abrir_disciplinas(tela_atual):
    print("Abrindo Minhas Disciplinas...")

def abrir_historico(tela_atual):
    print("Abrindo Histórico...")

def abrir_cursos(tela_atual):
    print("Abrindo Meus Cursos...")
    print("Abrindo Notas...")
    abrir_nova_tela(tela_atual,"notas_tela.py",False)

def abrir_notas(tela_atual):
    print("Abrindo Notas...")
    abrir_nova_tela(tela_atual,"notas_tela.py",False)

def abrir_desempenho(tela_atual):
    print("Abrindo Desempenho...")

def abrir_conta(tela_atual):
    print("Abrindo Conta...")

def criar_janela():
    root = tb.Window(themename="minty")
    root.title("Menu com Imagens")
    root.geometry("900x500")
    root.configure(bg="#c0f0d0")

    # Definindo um estilo personalizado para o Frame e outros widgets
    root.style.configure("my.TFrame", background="#c0f0d0")
    root.style.configure("my.TButton", font=("Arial", 10, "bold"), width=15, height=3)  # Ajuste o tamanho dos botões

    # Barra superior
    frame_topo = tb.Frame(root, bootstyle="light")
    frame_topo.pack(fill='x')
    
    lbl_usuario = tb.Label(frame_topo, text="Aluno Carlos", font=("Arial", 12, "bold"), bootstyle="black")
    lbl_usuario.pack(side="left", padx=20, pady=5)
    
    icon_config = Image.open("resources/icones/config.png")  # Substitua pelo ícone correto
    icon_config = icon_config.resize((30, 30))  # Redimensiona para 30x30 pixels
    icon_config = ImageTk.PhotoImage(icon_config)  # Converte para formato do tkinter

    btn_config = tb.Button(frame_topo, image=icon_config, bootstyle="light", command=lambda: abrir_config(root))
    btn_config.image = icon_config  # Para evitar garbage collection
    btn_config.pack(side="right", padx=10)

    # Título "Acesso Rápido"
    lbl_acesso_rapido = tb.Label(root, text="Acesso Rápido", font=("Arial", 12, "bold"), background="#c0f0d0")
    lbl_acesso_rapido.pack(pady=10)
    
    # Frame dos botões
    frame_botoes = tb.Frame(root, bootstyle="light", style="my.TFrame")  # Aplica o estilo personalizado
    frame_botoes.pack()

    botoes = [
        ("Minhas Disciplinas", "resources/icones/disciplinas.png", abrir_disciplinas),
        ("Histórico", "resources/icones/historico.png", abrir_historico),
        ("Meus Cursos", "resources/icones/cursos.png", abrir_cursos),
        ("Notas", "resources/icones/notas.png", abrir_notas),
        ("Desempenho", "resources/icones/desempenho.png", abrir_desempenho),
        ("Conta", "resources/icones/conta.png", abrir_conta)
    ]

    imagens = []  # Lista para armazenar referências das imagens

    for i, (titulo, img_path, funcao) in enumerate(botoes): 
        img = Image.open(img_path)  # Abre a imagem
        img = img.resize((150, 150), Image.Resampling.LANCZOS)  # Redimensiona para 30x30 pixels
        img = ImageTk.PhotoImage(img)  # Converte para formato do tkinter

        imagens.append(img)  # Armazena referência para evitar garbage collection

        # Redimensionando os botões e aplicando a cor de fundo
        btn = tb.Button(frame_botoes, text=titulo, image=img, compound="top", bootstyle="secondary", style="my.TButton", command=lambda funcao=funcao: funcao(root))
        btn.grid(row=i//3, column=i%3, padx=20, pady=10)

    # Vinculando a função on_close ao evento de fechar a janela
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))  # Chamando a função on_close

    root.mainloop()

if __name__ == "__main__":
    criar_janela()
