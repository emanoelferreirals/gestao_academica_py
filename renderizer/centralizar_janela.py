def centralizar_janela(root, largura, altura):
    # Obter a largura e altura da tela
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    print(f"l:{largura_tela}, a:{altura_tela}")
    
    # Calcular a posição x e y para centralizar a janela
    pos_x = (largura_tela // 2) - (largura // 2)
    pos_y = (altura_tela // 2) - (altura // 2) - 50
    
    # Definir as dimensões e a posição da janela
    root.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")